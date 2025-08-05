from data_access.database import get_db_connection
from mysql.connector import Error

class SeatRepository:
    def create_seats_for_room(self, room_id, capacity):
        conn, _ = get_db_connection()
        if conn is None:
            return 0
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM seats WHERE room_id = %s", (room_id,))
            existing_seats_count = cursor.fetchone()[0]

            if existing_seats_count >= capacity:
                return 0

            new_seats_to_add = capacity - existing_seats_count
            
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            seat_values = []
            
            for row_index in range(10): # 10 filas A-J
                row_letter = letters[row_index]
                for seat_number in range(1, 11): # 10 asientos por fila
                    seat_name = f"{row_letter}{seat_number}"
                    seat_values.append((seat_name, room_id))

            seats_to_insert = seat_values[:new_seats_to_add]

            if seats_to_insert:
                cursor.executemany("INSERT INTO seats (seat_name, room_id) VALUES (%s, %s)", seats_to_insert)
                conn.commit()
                return len(seats_to_insert)
            
            return 0
        except Error as e:
            print(f"Error al crear asientos para la sala {room_id}: {e}")
            if conn:
                conn.rollback()
            return 0
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_seats_by_room_id(self, room_id):
        conn, _ = get_db_connection()
        if conn is None:
            return []
        
        cursor = conn.cursor(dictionary=True)
        seats = []
        try:
            cursor.execute("""
                SELECT id, seat_name, room_id
                FROM seats
                WHERE room_id = %s
            """, (room_id,))
            seats = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener asientos para la sala {room_id}: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        return seats
    
    def get_seat_by_name_and_room_id(self, seat_name, room_id):
        conn, _ = get_db_connection()
        if conn is None:
            return None
        
        cursor = conn.cursor()
        seat_id = None
        try:
            cursor.execute("""
                SELECT id FROM seats WHERE seat_name = %s AND room_id = %s
            """, (seat_name, room_id))
            result = cursor.fetchone()
            if result:
                seat_id = result[0]
        except Error as e:
            print(f"Error al obtener asiento por nombre y sala: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        return seat_id
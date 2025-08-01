from data_access.database import get_db_connection
from mysql.connector import Error

class SeatRepository:

    def create_seats_for_room(self, room_id, capacity):

        conn = get_db_connection()
        if conn is None:
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            seats_added_count = 0
            for i in range(1, capacity + 1):

                row_char = chr(64 + ((i - 1) // 10) + 1)
                seat_number_in_row = (i - 1) % 10 + 1
                seat_name = f"{row_char}{seat_number_in_row}"

                cursor.execute('''
                    INSERT IGNORE INTO seats (room_id, seat_name)
                    VALUES (%s, %s)
                ''', (room_id, seat_name))
                if cursor.rowcount > 0:
                    seats_added_count += 1
            conn.commit()
            if seats_added_count > 0:
                print(f"Añadidos {seats_added_count} asientos (nuevos) para la sala ID {room_id}.")
            else:
                print(f"No se añadieron nuevos asientos para la sala ID {room_id} (ya existían).")
            return True
        except Error as e:
            print(f"Error al crear asientos para la sala {room_id}: {e}")
            conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_seats_by_room_id(self, room_id):

        conn = get_db_connection()
        if conn is None:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT id, room_id, seat_name
                FROM seats
                WHERE room_id = %s
            ''', (room_id,))
            seats = cursor.fetchall()
            return seats
        except Error as e:
            print(f"Error al obtener asientos para la sala {room_id}: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
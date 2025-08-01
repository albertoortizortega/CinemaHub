from data_access.database import get_db_connection
from mysql.connector import Error
from datetime import datetime

class SeatReservationRepository:

    def add_seat_reservation(self, session_id, seat_id):
        conn = get_db_connection()
        if conn is None:
            return None
        
        cursor = conn.cursor()
        try:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT INTO seat_reservations (session_id, seat_id, reservation_time)
                VALUES (%s, %s, %s)
            """, (session_id, seat_id, now))
            conn.commit()
            reservation_id = cursor.lastrowid
            print(f"Reserva para el asiento {seat_id} en la sesión {session_id} registrada con ID {reservation_id}.")
            return reservation_id
        except Error as e:
            # Error 1062 es para entradas duplicadas (UNIQUE constraint)
            if e.errno == 1062:
                print(f"Error: El asiento {seat_id} ya está reservado para la sesión {session_id}.")
            else:
                print(f"Error al registrar la reserva del asiento {seat_id}: {e}")
            conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_reserved_seats_for_session(self, session_id):
        conn = get_db_connection()
        if conn is None:
            return []
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT seat_id FROM seat_reservations
                WHERE session_id = %s
            """, (session_id,))
            reserved_seats = cursor.fetchall()
            return [seat['seat_id'] for seat in reserved_seats]
        except Error as e:
            print(f"Error al obtener los asientos reservados para la sesión {session_id}: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_reservation_by_id(self, reservation_id):
        conn = get_db_connection()
        if conn is None:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id, session_id, seat_id, reservation_time
                FROM seat_reservations
                WHERE id = %s
            """, (reservation_id,))
            reservation = cursor.fetchone()
            return reservation
        except Error as e:
            print(f"Error al obtener la reserva con ID {reservation_id}: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
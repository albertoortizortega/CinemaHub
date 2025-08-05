from data_access.database import get_db_connection
from mysql.connector import Error
from datetime import datetime

class SeatReservationRepository:
    def add_seat_reservation(self, session_id, seat_id):
        conn, _ = get_db_connection()
        if conn is None: return None
        
        cursor = conn.cursor()
        try:
            now = datetime.now()
            cursor.execute("""
                INSERT INTO seat_reservations (session_id, seat_id, reservation_time)
                VALUES (%s, %s, %s)
            """, (session_id, seat_id, now))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al añadir reserva: {e}")
            conn.rollback()
            return None
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_reserved_seats_for_session(self, session_id):
        conn, _ = get_db_connection()
        if conn is None: return set()
        
        cursor = conn.cursor()
        reserved_seats = set()
        try:
            cursor.execute("""
                SELECT seat_id FROM seat_reservations WHERE session_id = %s
            """, (session_id,))
            for (seat_id,) in cursor.fetchall():
                reserved_seats.add(seat_id)
        except Error as e:
            print(f"Error al obtener asientos reservados para la sesión {session_id}: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()
        return reserved_seats
from data_access.database import get_db_connection
from mysql.connector import Error
from datetime import datetime

class SessionRepository:

    def add_session(self, movie_id, room_id, start_time_str, end_time_str, price):

        conn = get_db_connection()
        if conn is None:
            return None

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sessions (movie_id, room_id, start_time, end_time, price)
                VALUES (%s, %s, %s, %s, %s)
            ''', (movie_id, room_id, start_time_str, end_time_str, price))
            conn.commit()
            session_id = cursor.lastrowid
            return session_id
        except Error as e:
            print(f"Error al añadir sesión: {e}")
            conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_all_sessions(self):
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT
                    s.id,
                    s.movie_id,
                    m.title AS movie_title,
                    s.room_id,
                    r.name AS room_name,
                    s.start_time,
                    s.end_time,
                    s.price
                FROM sessions s
                JOIN movies m ON s.movie_id = m.id
                JOIN rooms r ON s.room_id = r.id
                ORDER BY s.start_time
            ''')
            sessions = cursor.fetchall()
            return sessions
        except Error as e:
            print(f"Error al obtener todas las sesiones: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_session_by_id(self, session_id):
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT
                    s.id,
                    s.movie_id,
                    m.title AS movie_title,
                    s.room_id,
                    r.name AS room_name,
                    s.start_time,
                    s.end_time,
                    s.price
                FROM sessions s
                JOIN movies m ON s.movie_id = m.id
                JOIN rooms r ON s.room_id = r.id
                WHERE s.id = %s
            ''', (session_id,))
            session = cursor.fetchone()
            return session
        except Error as e:
            print(f"Error al obtener sesión por ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_sessions_by_room_id(self, room_id):
        conn = get_db_connection()
        if conn is None:
            return []
        
        cursor = conn.cursor(dictionary=True)
        sessions = []
        try:
            cursor.execute("""
                SELECT id, movie_id, room_id, start_time, end_time, price 
                FROM sessions 
                WHERE room_id = %s
            """, (room_id,))
            sessions = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener sesiones para la sala {room_id}: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()
        return sessions

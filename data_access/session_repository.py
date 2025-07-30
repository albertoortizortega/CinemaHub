from data_access.database import get_db_connection
from mysql.connector import Error
from datetime import datetime

class SessionRepository:
    """
    Clase que encapsula las operaciones CRUD para la tabla 'sessions' en la base de datos MySQL.
    """

    def add_session(self, movie_id, room_id, start_time_str, end_time_str, price):
        """
        Añade una nueva sesión de cine a la tabla 'sessions'.
        Los tiempos deben ser cadenas en formato 'YYYY-MM-DD HH:MM:SS'.

        Args:
            movie_id (int): ID de la película asociada a la sesión.
            room_id (int): ID de la sala donde se proyecta la sesión.
            start_time_str (str): Hora de inicio de la sesión (formato 'YYYY-MM-DD HH:MM:SS').
            end_time_str (str): Hora de fin de la sesión (formato 'YYYY-MM-DD HH:MM:SS').
            price (float): Precio de la entrada para esta sesión.

        Returns:
            int or None: El ID de la sesión recién insertada si es exitoso, None en caso de error.
        """
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
        """
        Obtiene todas las sesiones de la tabla 'sessions', incluyendo detalles de la película y la sala.

        Returns:
            list: Una lista de diccionarios, donde cada diccionario representa una sesión con detalles.
                  Retorna una lista vacía si no hay sesiones o si ocurre un error.
        """
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
        """
        Obtiene una sesión específica por su ID, incluyendo detalles de la película y la sala.
        """
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
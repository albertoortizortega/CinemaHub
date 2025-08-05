from data_access.database import get_db_connection
from mysql.connector import Error

class MovieRepository:
    def add_movie(self, title, duration, genre, director, synopsis):
        conn, _ = get_db_connection()
        if conn is None: return None
        
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO movies (title, duration_minutes, genre, director, synopsis) 
                VALUES (%s, %s, %s, %s, %s)
            """, (title, duration, genre, director, synopsis))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al añadir película: {e}")
            conn.rollback()
            return None
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_movie_by_id(self, movie_id):
        conn, _ = get_db_connection()
        if conn is None: return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al obtener película por ID: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_movie_by_title(self, title):
        conn, _ = get_db_connection()
        if conn is None: return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM movies WHERE title = %s", (title,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al obtener película por título: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_all_movies(self):
        conn, _ = get_db_connection()
        if conn is None: return []
        
        cursor = conn.cursor(dictionary=True)
        movies = []
        try:
            cursor.execute("SELECT * FROM movies")
            movies = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener todas las películas: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()
        return movies
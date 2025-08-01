from data_access.database import get_db_connection
from mysql.connector import Error

class MovieRepository:

    def add_movie(self, title, duration_minutes, genre=None, director=None, synopsis=None):
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO movies (title, duration_minutes, genre, director, synopsis)
                VALUES (%s, %s, %s, %s, %s)
            ''', (title, duration_minutes, genre, director, synopsis))
            conn.commit()
            movie_id = cursor.lastrowid
            return movie_id
        except Error as e:
            print(f"Error al añadir película '{title}': {e}")
            conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_all_movies(self):
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM movies')
            movies = cursor.fetchall()
            return movies
        except Error as e:
            print(f"Error al obtener todas las películas: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_movie_by_id(self, movie_id):
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM movies WHERE id = %s', (movie_id,))
            movie = cursor.fetchone()
            return movie
        except Error as e:
            print(f"Error al obtener película por ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_movie_by_title(self, title):
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM movies WHERE title = %s', (title,))
            movie = cursor.fetchone()
            return movie
        except Error as e:
            print(f"Error al obtener película por título: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
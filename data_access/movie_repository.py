from data_access.database import get_db_connection
from mysql.connector import Error

class MovieRepository:
    """
    Clase que encapsula las operaciones CRUD (Crear, Leer, Actualizar, Borrar)
    para la tabla 'movies' en la base de datos MySQL.
    """

    def add_movie(self, title, duration_minutes, genre=None, director=None, synopsis=None):
        """
        Añade una nueva película a la tabla 'movies'.

        Args:
            title (str): Título de la película.
            duration_minutes (int): Duración de la película en minutos.
            genre (str, optional): Género de la película. Defaults to None.
            director (str, optional): Director de la película. Defaults to None.
            synopsis (str, optional): Sinopsis de la película. Defaults to None.

        Returns:
            int or None: El ID de la película recién insertada si es exitoso, None en caso de error.
        """
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
        """
        Obtiene todas las películas de la tabla 'movies'.

        Returns:
            list: Una lista de diccionarios, donde cada diccionario representa una película.
                  Retorna una lista vacía si no hay películas o si ocurre un error.
        """
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
        """
        Obtiene una película específica por su ID.
        """
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
        """
        Obtiene una película específica por su título.
        Útil para verificar si una película ya existe antes de añadirla.
        """
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
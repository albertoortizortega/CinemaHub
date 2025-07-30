from data_access.database import get_db_connection
from mysql.connector import Error

class RoomRepository:
    """
    Clase que encapsula las operaciones CRUD para la tabla 'rooms' en la base de datos MySQL.
    """

    def add_room(self, name, capacity):
        """
        Añade una nueva sala a la tabla 'rooms'.
        """
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO rooms (name, capacity)
                VALUES (%s, %s)
            ''', (name, capacity))
            conn.commit()
            room_id = cursor.lastrowid
            return room_id
        except Error as e:
            if e.errno == 1062:
                print(f"Error: La sala con nombre '{name}' ya existe.")
            else:
                print(f"Error al añadir sala '{name}': {e}")
            conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_all_rooms(self):
        """
        Obtiene todas las salas de la tabla 'rooms'.
        """
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM rooms')
            rooms = cursor.fetchall()
            return rooms
        except Error as e:
            print(f"Error al obtener todas las salas: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_room_by_id(self, room_id):
        """
        Obtiene una sala específica por su ID.
        """
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM rooms WHERE id = %s', (room_id,))
            room = cursor.fetchone()
            return room
        except Error as e:
            print(f"Error al obtener sala por ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_room_by_name(self, name):
        """
        Obtiene una sala específica por su nombre.
        Útil para verificar si una sala ya existe antes de añadirla.
        """
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM rooms WHERE name = %s', (name,))
            room = cursor.fetchone()
            return room
        except Error as e:
            print(f"Error al obtener sala por nombre: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
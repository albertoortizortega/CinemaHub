from data_access.database import get_db_connection
from mysql.connector import Error

class RoomRepository:
    def add_room(self, name, capacity):
        conn, _ = get_db_connection()
        if conn is None: return None
        
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO rooms (name, capacity) VALUES (%s, %s)", (name, capacity))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al añadir sala: {e}")
            conn.rollback()
            return None
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_room_by_id(self, room_id):
        conn, _ = get_db_connection()
        if conn is None: return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al obtener sala por ID: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_room_by_name(self, name):
        conn, _ = get_db_connection()
        if conn is None: return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM rooms WHERE name = %s", (name,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al obtener sala por nombre: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_all_rooms(self):
        conn, _ = get_db_connection()
        if conn is None: return []
        
        cursor = conn.cursor(dictionary=True)
        rooms = []
        try:
            cursor.execute("SELECT * FROM rooms")
            rooms = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener todas las salas: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected():
                conn.close()
        return rooms
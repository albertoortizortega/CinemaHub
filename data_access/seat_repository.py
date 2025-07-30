from data_access.database import get_db_connection
from mysql.connector import Error

class SeatRepository:
    """
    Clase que encapsula las operaciones CRUD para la tabla 'seats' en la base de datos MySQL.
    Se enfoca en la gestión de los asientos dentro de las salas.
    """

    def create_seats_for_room(self, room_id, capacity):
        """
        Crea un número específico de asientos para una sala dada.
        Se asume que los asientos se nombran secuencialmente (ej. 'A1', 'A2', ...).
        Esta es una operación para poblar inicialmente los asientos de una sala.
        Utiliza INSERT IGNORE para evitar duplicados si se ejecuta varias veces.

        Args:
            room_id (int): El ID de la sala para la que se crean los asientos.
            capacity (int): El número total de asientos que debe tener la sala.

        Returns:
            bool: True si la operación fue exitosa, False en caso de error.
        """
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
        """
        Obtiene todos los asientos asociados a una sala específica.

        Args:
            room_id (int): El ID de la sala.

        Returns:
            list: Una lista de diccionarios, donde cada diccionario representa un asiento.
                  Retorna una lista vacía si no hay asientos o si ocurre un error.
        """
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
                ORDER BY seat_name
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
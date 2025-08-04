import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'database': 'mysql',
    'user': 'root',
    'password': '123456'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print(f"Conexión exitosa a la base de datos {DB_CONFIG['database']}")
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        return None

def create_tables():
    conn = get_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        # Definición de la tabla 'movies'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL UNIQUE,
                duration_minutes INT,
                genre VARCHAR(100),
                director VARCHAR(255),
                synopsis TEXT
            );
        """)

        # Definición de la tabla 'rooms'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                capacity INT NOT NULL
            );
        """)

        # Definición de la tabla 'sessions'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT NOT NULL,
                room_id INT NOT NULL,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                price DECIMAL(5, 2) NOT NULL,
                FOREIGN KEY (movie_id) REFERENCES movies(id),
                FOREIGN KEY (room_id) REFERENCES rooms(id)
            );
        """)

        # Definición de la tabla 'seats'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_id INT NOT NULL,
                seat_name VARCHAR(10) NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms(id),
                UNIQUE (room_id, seat_name)
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seat_reservations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                session_id INT NOT NULL,
                seat_id INT NOT NULL,
                reservation_time DATETIME NOT NULL,
                -- Agregamos un campo para saber qué usuario hizo la reserva
                user_id INT,
                FOREIGN KEY (session_id) REFERENCES sessions(id),
                FOREIGN KEY (seat_id) REFERENCES seats(id),
                UNIQUE (session_id, seat_id)
            );
        """)

        print("Tablas verificadas y listas en MySQL.")
        
        # Opcional: Insertar una sala principal por defecto si no existe
        cursor.execute("INSERT IGNORE INTO rooms (name, capacity) VALUES ('Sala Principal', 100);")
        conn.commit()

    except Error as e:
        print(f"Error al crear tablas: {e}")
        conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    create_tables()
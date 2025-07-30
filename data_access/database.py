import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'database': 'cinemahub',
    'user': 'root',
    'password': 'BDII2023'
}

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print(f"Conexión exitosa a la base de datos {DB_CONFIG['database']}")
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        return None

def create_tables():
    """Crea las tablas necesarias en la base de datos si no existen."""
    conn = get_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                duration_minutes INT NOT NULL,
                genre VARCHAR(100),
                director VARCHAR(255),
                synopsis TEXT
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                capacity INT NOT NULL
            );
        ''')
        cursor.execute("INSERT IGNORE INTO rooms (id, name, capacity) VALUES (1, 'Sala Principal', 100)")


        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT NOT NULL,
                room_id INT NOT NULL,
                start_time DATETIME NOT NULL, -- Usamos DATETIME para fechas y horas
                end_time DATETIME NOT NULL,
                price DECIMAL(5, 2) NOT NULL, -- DECIMAL para precios
                FOREIGN KEY (movie_id) REFERENCES movies(id),
                FOREIGN KEY (room_id) REFERENCES rooms(id)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                session_id INT NOT NULL,
                seat_number VARCHAR(10) NOT NULL, -- Ej: 'A1', 'B5'
                is_booked BOOLEAN NOT NULL DEFAULT FALSE, -- BOOLEAN en MySQL
                FOREIGN KEY (session_id) REFERENCES sessions(id),
                UNIQUE (session_id, seat_number) -- Asegura que un asiento es único por sesión
            );
        ''')

        conn.commit()
        print("Tablas verificadas y listas en MySQL.")

    except Error as e:
        print(f"Error al crear tablas: {e}")
        conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión a MySQL cerrada.")

if __name__ == '__main__':
    create_tables()
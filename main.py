from data_access.database import create_tables, get_db_connection
from data_access.movie_repository import MovieRepository
from data_access.room_repository import RoomRepository
from data_access.session_repository import SessionRepository
from mysql.connector import Error
from datetime import datetime, timedelta


def initialize_app():
    """
    Función para inicializar los componentes esenciales de la aplicación.
    Se encarga de asegurar que las tablas de la DB existan.
    """
    print("\n--- Iniciando CinemaHub ---")
    create_tables()
    print("Base de datos verificada y tablas listas.")


def populate_and_list_movies():
    """
    Función para añadir películas de prueba directamente y luego listarlas,
    evitando duplicados por título.
    """
    print("\n--- Poblando y listando películas ---")

    movie_repo = MovieRepository()

    movies_to_add = [
        ("El Padrino", 175, "Crimen, Drama", "Francis Ford Coppola", "La épica saga de la familia Corleone y su imperio criminal en Nueva York."),
        ("Oppenheimer", 180, "Biografía, Drama, Historia", "Christopher Nolan", "La historia del científico J. Robert Oppenheimer y su papel en el desarrollo de la bomba atómica."),
        ("La La Land", 128, "Musical, Drama, Romance", "Damien Chazelle", "Una aspirante a actriz y un músico de jazz se enamoran en Los Ángeles."),
        ("Parasitos", 132, "Comedia Negra, Thriller", "Bong Joon-ho", "Una familia pobre se infiltra en la vida de una familia rica."),
        ("Interestelar", 169, "Ciencia Ficción, Drama", "Christopher Nolan", "Un equipo de exploradores viaja a través de un agujero de gusano para salvar a la humanidad."),
        ("Forrest Gump", 142, "Comedia, Drama, Romance", "Robert Zemeckis", "La vida de un hombre sencillo a lo largo de eventos históricos de EE.UU."),
        ("El Gran Dictador", 125, "Comedia, Sátira", "Charles Chaplin", "Un barbero judío idéntico a un dictador se ve envuelto en suplantación de identidad."),
        ("Vértigo", 128, "Thriller, Misterio", "Alfred Hitchcock", "Un detective retirado con miedo a las alturas investiga a una mujer misteriosa.")
    ]

    print("Añadiendo películas de prueba (solo si no existen por título)...")
    for title, duration, genre, director, synopsis in movies_to_add:
        if not movie_repo.get_movie_by_title(title):
            movie_repo.add_movie(title, duration, genre, director, synopsis)
            print(f"Añadida: '{title}'")

    print("\n--- Películas actualmente en la base de datos ---")
    all_movies = movie_repo.get_all_movies()
    if all_movies:
        for movie in all_movies:
            print(f"- ID: {movie.get('id', 'N/A')}, Título: {movie.get('title', 'N/A')} ({movie.get('duration_minutes', 'N/A')} min), Género: {movie.get('genre', 'N/A')}")
    else:
        print("No se encontraron películas en la base de datos.")

    print("\n--- Poblamiento y listado de películas completado ---")


def populate_and_list_rooms():
    """
    Función para añadir salas de prueba directamente y luego listarlas,
    evitando duplicados por nombre.
    """
    print("\n--- Poblando y listando salas ---")

    room_repo = RoomRepository()

    rooms_to_add = [
        ("Sala 2", 75),
        ("Sala VIP", 30)
    ]

    print("Añadiendo salas de prueba (solo si no existen por nombre)...")
    for name, capacity in rooms_to_add:
        if not room_repo.get_room_by_name(name):
            room_repo.add_room(name, capacity)
            print(f"Añadida: '{name}'")

    print("\n--- Salas actualmente en la base de datos ---")
    all_rooms = room_repo.get_all_rooms()
    if all_rooms:
        for room in all_rooms:
            print(f"- ID: {room.get('id', 'N/A')}, Nombre: {room.get('name', 'N/A')}, Capacidad: {room.get('capacity', 'N/A')}")
    else:
        print("No se encontraron salas en la base de datos.")

    print("\n--- Poblamiento y listado de salas completado ---")


def populate_and_list_sessions():
    """
    Función para añadir sesiones de prueba y luego listarlas.
    Las sesiones se añadirán cada vez que se ejecute si no hay una comprobación
    más compleja de duplicados por (película, sala, hora de inicio).
    Para este desarrollo inicial, permitimos que se añadan si se ejecuta varias veces,
    o puedes usar la opción de vaciar la tabla de sesiones.
    """
    print("\n--- Poblando y listando sesiones ---")

    movie_repo = MovieRepository()
    room_repo = RoomRepository()
    session_repo = SessionRepository()

    movies = movie_repo.get_all_movies()
    rooms = room_repo.get_all_rooms()

    if not movies:
        print("No hay películas disponibles para crear sesiones. Ejecuta 'populate_and_list_movies' primero.")
        return
    if not rooms:
        print("No hay salas disponibles para crear sesiones. Ejecuta 'populate_and_list_rooms' primero.")
        return

    el_padrino_id = next((m['id'] for m in movies if m['title'] == 'El Padrino'), None)
    oppenheimer_id = next((m['id'] for m in movies if m['title'] == 'Oppenheimer'), None)
    interstellar_id = next((m['id'] for m in movies if m['title'] == 'Interestelar'), None)

    sala_principal_id = next((r['id'] for r in rooms if r['name'] == 'Sala Principal'), None)
    sala_2_id = next((r['id'] for r in rooms if r['name'] == 'Sala 2'), None)
    sala_vip_id = next((r['id'] for r in rooms if r['name'] == 'Sala VIP'), None)

    if not all([el_padrino_id, oppenheimer_id, interstellar_id, sala_principal_id, sala_2_id, sala_vip_id]):
        print("¡Advertencia! No se encontraron todas las IDs de películas o salas necesarias para crear sesiones. "
              "Asegúrate de que los nombres y títulos en 'movies_to_add' y 'rooms_to_add' coincidan y que se hayan insertado.")
        
        if not el_padrino_id and len(movies) > 0: el_padrino_id = movies[0]['id']
        if not oppenheimer_id and len(movies) > 1: oppenheimer_id = movies[1]['id']
        if not interstellar_id and len(movies) > 2: interstellar_id = movies[2]['id']

        if not sala_principal_id and len(rooms) > 0: sala_principal_id = rooms[0]['id']
        if not sala_2_id and len(rooms) > 1: sala_2_id = rooms[1]['id']
        if not sala_vip_id and len(rooms) > 2: sala_vip_id = rooms[2]['id']

        if not all([el_padrino_id, oppenheimer_id, interstellar_id, sala_principal_id, sala_2_id, sala_vip_id]):
             print("No hay suficientes datos válidos para crear todas las sesiones de prueba.")
             return


    print("Añadiendo sesiones de prueba...")
    now = datetime.now()
    
    today_date_str = now.strftime('%Y-%m-%d')

    sessions_data = [
        # (movie_id, room_id, start_time, end_time, price)
        (el_padrino_id, sala_principal_id, f"{today_date_str} 19:00:00", f"{today_date_str} 21:55:00", 8.50), # 175 min
        (oppenheimer_id, sala_2_id, f"{today_date_str} 20:00:00", f"{today_date_str} 23:00:00", 9.00), # 180 min
        (interstellar_id, sala_vip_id, f"{today_date_str} 21:00:00", f"{today_date_str} 23:49:00", 12.00) # 169 min
    ]

    for movie_id, room_id, start_time_str, end_time_str, price in sessions_data:
        
        session_repo.add_session(movie_id, room_id, start_time_str, end_time_str, price)
        


    print("\n--- Sesiones actualmente en la base de datos ---")
    all_sessions = session_repo.get_all_sessions()
    if all_sessions:
        for session in all_sessions:
            print(f"- ID: {session.get('id', 'N/A')}, Película: {session.get('movie_title', 'N/A')} "
                  f"en {session.get('room_name', 'N/A')} "
                  f"desde {session.get('start_time', 'N/A')} hasta {session.get('end_time', 'N/A')} - Precio: {session.get('price', 'N/A')}€")
    else:
        print("No se encontraron sesiones en la base de datos.")

    print("\n--- Poblamiento y listado de sesiones completado ---")


def truncate_all_tables():
    """
    Vacía todas las tablas de datos (seats, sessions, movies, rooms) para empezar de cero.
    ¡CUIDADO! Esto eliminará todos los datos.
    """
    print("\n--- Vaciando tablas de la base de datos ---")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None: return

        cursor = conn.cursor()
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE seats;")
        cursor.execute("TRUNCATE TABLE sessions;")
        cursor.execute("TRUNCATE TABLE movies;")
        cursor.execute("TRUNCATE TABLE rooms;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        print("Todas las tablas (seats, sessions, movies, rooms) han sido vaciadas exitosamente.")
    except Error as e:
        print(f"Error al vaciar tablas: {e}")
        if conn: conn.rollback()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()


if __name__ == "__main__":
    
    user_input = input("¿Vaciar todas las tablas de datos (películas, salas, sesiones, asientos) antes de poblar? (s/n): ").lower()
    if user_input == 's':
        truncate_all_tables()
        
        initialize_app()
    else:
        initialize_app()

    populate_and_list_movies()
    populate_and_list_rooms()
    populate_and_list_sessions()

    print("\n--- CinemaHub ha completado su ejecución inicial ---")
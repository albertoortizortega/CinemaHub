
from data_access.database import create_tables, get_db_connection
from data_access.movie_repository import MovieRepository
from data_access.room_repository import RoomRepository
from data_access.session_repository import SessionRepository
from data_access.seat_repository import SeatRepository
from business_logic.cinema_manager import CinemaManager
from mysql.connector import Error
from datetime import datetime, timedelta

def initialize_app():
    print("\n--- Iniciando CinemaHub ---")
    create_tables()
    print("Base de datos verificada y tablas listas.")

def truncate_all_tables():
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
        print("Todas las tablas han sido vaciadas exitosamente.")
    except Error as e:
        print(f"Error al vaciar tablas: {e}")
        if conn: conn.rollback()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()

def populate_movies(manager):
    print("\n--- Poblando películas ---")
    movies_to_add = [
        ("El Padrino", 175, "Crimen, Drama", "Francis Ford Coppola", "La épica saga de la familia Corleone y su imperio criminal en Nueva York."),
        ("Oppenheimer", 180, "Biografía, Drama, Historia", "Christopher Nolan", "La historia del científico J. Robert Oppenheimer y su papel en el desarrollo de la bomba atómica.")
    ]
    for title, duration, genre, director, synopsis in movies_to_add:
        if not manager.movie_repo.get_movie_by_title(title):
            manager.movie_repo.add_movie(title, duration, genre, director, synopsis)

def populate_rooms(manager):
    print("\n--- Poblando salas ---")
    rooms_to_add = [("Sala 2", 75), ("Sala VIP", 30)]
    for name, capacity in rooms_to_add:
        if not manager.room_repo.get_room_by_name(name):
            manager.room_repo.add_room(name, capacity)

def populate_sessions_and_seats(manager):
    print("\n--- Poblando sesiones y asientos ---")
    movies = manager.movie_repo.get_all_movies()
    rooms = manager.room_repo.get_all_rooms()

    if not movies or not rooms:
        print("Advertencia: No hay películas o salas para poblar.")
        return

    el_padrino_id = next((m['id'] for m in movies if m['title'] == 'El Padrino'), None)
    sala_principal_id = next((r['id'] for r in rooms if r['name'] == 'Sala Principal'), None)
    
    if el_padrino_id and sala_principal_id:
        today_date_str = datetime.now().strftime('%Y-%m-%d')
        manager.schedule_new_session(el_padrino_id, sala_principal_id, f"{today_date_str} 19:00:00", 8.50)

    for room in rooms:
        manager.seat_repo.create_seats_for_room(room['id'], room['capacity'])


# Bloque principal de ejecución
if __name__ == "__main__":
    user_input = input("¿Vaciar todas las tablas de datos? (s/n): ").lower()
    if user_input == 's':
        truncate_all_tables()
    
    initialize_app()
    cinema_manager = CinemaManager()
    
    populate_movies(cinema_manager)
    populate_rooms(cinema_manager)
    populate_sessions_and_seats(cinema_manager)

    print("\n--- Pruebas de lógica de negocio ---")
    movies = cinema_manager.get_available_movies()
    rooms = cinema_manager.room_repo.get_all_rooms()
    sessions = cinema_manager.get_all_sessions_details()

    el_padrino_id = next((m['id'] for m in movies if m['title'] == 'El Padrino'), None)
    sala_principal_id = next((r['id'] for r in rooms if r['name'] == 'Sala Principal'), None)
    first_session_id = next((s['id'] for s in sessions if s['room_name'] == 'Sala Principal'), None)
    
    if el_padrino_id and sala_principal_id and first_session_id:
        print(f"\nProbando agendar una sesión en Sala Principal a las 22:00 (no solapa)...")
        start_time_no_overlap = f"{datetime.now().strftime('%Y-%m-%d')} 22:00:00"
        new_session_id = cinema_manager.schedule_new_session(el_padrino_id, sala_principal_id, start_time_no_overlap, 10.00)
        
        print(f"\nProbando agendar una sesión en Sala Principal a las 19:30 (SÍ solapa)...")
        start_time_overlap = f"{datetime.now().strftime('%Y-%m-%d')} 19:30:00"
        cinema_manager.schedule_new_session(el_padrino_id, sala_principal_id, start_time_overlap, 11.00)

        print(f"\nProbando reserva de asiento ID 1 para la sesión {first_session_id} (debe ser exitoso)...")
        cinema_manager.book_seat(first_session_id, 1)

        print(f"Probando reservar el mismo asiento (ID 1) de nuevo (debe fallar)...")
        cinema_manager.book_seat(first_session_id, 1)

    print("\n--- Mostrando estado de los asientos para la sesión 1 ---")
    if first_session_id:
        seat_status = cinema_manager.get_session_seat_status(first_session_id)
        if seat_status:
            for seat in seat_status:
                print(f"Asiento: {seat['seat_name']} (ID: {seat['seat_id']}) - Estado: {seat['status']}")
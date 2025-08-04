from data_access.database import create_tables
from business_logic.cinema_manager import CinemaManager
from utils.db_initializer import truncate_all_tables, populate_movies, populate_rooms, populate_sessions_and_seats
from datetime import datetime

def initialize_app():
    """
    Inicializa la base de datos y la aplicación.
    """
    print("\n--- Iniciando CinemaHub ---")
    create_tables()
    print("Base de datos verificada y tablas listas.")

def run_tests(cinema_manager):
    """
    Ejecuta un conjunto de pruebas de lógica de negocio.
    """
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
        cinema_manager.schedule_new_session(el_padrino_id, sala_principal_id, start_time_no_overlap, 10.00)
        
        print(f"\nProbando agendar una sesión en Sala Principal a las 19:30 (SÍ solapa)...")
        start_time_overlap = f"{datetime.now().strftime('%Y-%m-%d')} 19:30:00"
        cinema_manager.schedule_new_session(el_padrino_id, sala_principal_id, start_time_overlap, 11.00)

        print(f"\nProbando reserva de asiento ID 1 para la sesión {first_session_id} (debe ser exitoso)...")
        cinema_manager.book_seat(first_session_id, 1)

        print(f"Probando reservar el mismo asiento (ID 1) de nuevo (debe fallar)...")
        cinema_manager.book_seat(first_session_id, 1)

        print("\n--- Mostrando estado de los asientos para la sesión 1 ---")
        seat_status = cinema_manager.get_session_seat_status(first_session_id)
        if seat_status:
            for seat in seat_status:
                print(f"Asiento: {seat['seat_name']} (ID: {seat['seat_id']}) - Estado: {seat['status']}")

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

    run_tests(cinema_manager)
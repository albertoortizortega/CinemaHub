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

def show_menu():
    """Muestra el menú de opciones al usuario."""
    print("\n--- Menú de CinemaHub ---")
    print("1. Ver películas disponibles")
    print("2. Ver todas las sesiones")
    print("3. Ver asientos de una sesión y reservar")
    print("4. Agendar nueva sesión (Solo para admins)")
    print("0. Salir")
    return input("Elige una opción: ")

def handle_choice(choice, manager):
    """Maneja la opción seleccionada por el usuario."""
    if choice == '1':
        movies = manager.get_available_movies()
        print("\n--- Películas Disponibles ---")
        for movie in movies:
            print(f"ID: {movie['id']}, Título: {movie['title']}, Duración: {movie['duration_minutes']} min")

    elif choice == '2':
        sessions = manager.get_all_sessions_details()
        print("\n--- Todas las Sesiones ---")
        for session in sessions:
            print(f"ID: {session['id']}, Película: {session['movie_title']}, Sala: {session['room_name']}, Hora: {session['start_time'].strftime('%H:%M')}, Precio: {session['price']}€")

    elif choice == '3':
        session_id = input("Introduce el ID de la sesión para ver asientos: ")
        try:
            session_id = int(session_id)
            seat_status = manager.get_session_seat_status(session_id)
            if seat_status:
                print(f"\n--- Asientos para la Sesión ID {session_id} ---")
                for seat in seat_status:
                    print(f"Asiento: {seat['seat_name']} (ID: {seat['seat_id']}) - Estado: {seat['status']}")
                
                seat_id = input("Introduce el ID del asiento que quieres reservar (o presiona Enter para cancelar): ")
                if seat_id:
                    seat_id = int(seat_id)
                    manager.book_seat(session_id, seat_id)
        except ValueError:
            print("Entrada no válida. Por favor, introduce un número.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    elif choice == '4':
        try:
            movie_id = int(input("ID de la película: "))
            room_id = int(input("ID de la sala: "))
            start_time_str = input("Hora de inicio (YYYY-MM-DD HH:MM:SS): ")
            price = float(input("Precio: "))
            manager.schedule_new_session(movie_id, room_id, start_time_str, price)
        except ValueError:
            print("Entrada no válida. Asegúrate de introducir números donde corresponde.")

# Bloque principal de ejecución
if __name__ == "__main__":
    user_input = input("¿Vaciar y poblar la base de datos con datos de prueba? (s/n): ").lower()
    if user_input == 's':
        truncate_all_tables()
        initialize_app()
        cinema_manager = CinemaManager()
        populate_movies(cinema_manager)
        populate_rooms(cinema_manager)
        populate_sessions_and_seats(cinema_manager)
    else:
        initialize_app()
        cinema_manager = CinemaManager()
        print("Base de datos inicializada. Se usarán los datos existentes.")

    while True:
        user_choice = show_menu()
        if user_choice == '0':
            print("Saliendo de CinemaHub. ¡Hasta pronto!")
            break
        handle_choice(user_choice, cinema_manager)
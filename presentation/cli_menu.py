from business_logic.cinema_manager import CinemaManager
from datetime import datetime

def show_menu():
    print("\n--- Menú de CinemaHub ---")
    print("1. Ver películas disponibles")
    print("2. Ver todas las sesiones")
    print("3. Ver asientos de una sesión y reservar")
    print("4. Agendar nueva sesión (Solo para admins)")
    print("0. Salir")
    return input("Elige una opción: ")

def handle_choice(choice, manager):
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
        session_id = input("Introduce el ID de la sesión para ver asientos y reservar: ")
        try:
            session_id = int(session_id)
            session_details = manager.get_session_seat_status(session_id)
            if session_details:
                print("\n--- Detalles de la Sesión ---")
                print(f"Película: {session_details['movie_title']}")
                print(f"Sala: {session_details['room_name']}")
                print(f"Hora: {session_details['start_time'].strftime('%H:%M')} (Precio: {session_details['price']}€)")
                
                print("\n--- Estado de los Asientos ---")
                seats_per_row = 10
                for i, seat in enumerate(session_details['seats'], 1):
                    status_char = 'X' if seat['status'] == 'Reservado' else 'O'
                    print(f"[{status_char}] {seat['seat_name']}".ljust(10), end='')
                    if i % seats_per_row == 0:
                        print()
                print()

                seat_name = input("Introduce el nombre del asiento que quieres reservar (ej. A1): ")
                if seat_name:
                    manager.book_seat(session_id, seat_name.upper())
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

def run_cli_app():
    user_choice = show_menu()
    if user_choice == '0':
        print("Saliendo de CinemaHub. ¡Hasta pronto!")
        return False
    handle_choice(user_choice, CinemaManager())
    return True
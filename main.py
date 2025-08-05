from data_access.database import create_tables, get_db_connection
from business_logic.cinema_manager import CinemaManager
from utils.db_initializer import truncate_all_tables, populate_movies, populate_rooms, populate_sessions_and_seats
from presentation.cli_menu import show_menu, handle_choice

def initialize_app():
    print("\n--- Iniciando CinemaHub ---")
    conn, message = get_db_connection()
    if conn:
        print(message)
        conn.close()
    create_tables()

# Bloque principal de ejecución
if __name__ == "__main__":
    user_input = input("¿Vaciar y poblar la base de datos con datos de prueba? (s/n): ").lower()
    
    cinema_manager = CinemaManager()
    
    if user_input == 's':
        truncate_all_tables()
        initialize_app()
        populate_movies(cinema_manager)
        populate_rooms(cinema_manager)
        populate_sessions_and_seats(cinema_manager)
        print("\n--- Poblamiento de datos de prueba finalizado con éxito. ---")
    else:
        initialize_app()
        print("Base de datos inicializada. Se usarán los datos existentes.")

    while True:
        user_choice = show_menu()
        if user_choice == '0':
            print("Saliendo de CinemaHub. ¡Hasta pronto!")
            break
        handle_choice(user_choice, cinema_manager)
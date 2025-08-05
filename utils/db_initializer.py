# utils/db_initializer.py

from data_access.database import get_db_connection
from business_logic.cinema_manager import CinemaManager
from mysql.connector import Error
from datetime import datetime

def truncate_all_tables():
    print("\n--- Vaciando tablas de la base de datos ---")
    conn = None
    cursor = None
    try:
        conn, _ = get_db_connection()
        if conn is None: return

        cursor = conn.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE seats;")
        cursor.execute("TRUNCATE TABLE sessions;")
        cursor.execute("TRUNCATE TABLE movies;")
        cursor.execute("TRUNCATE TABLE rooms;")
        cursor.execute("TRUNCATE TABLE seat_reservations;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
    except Error as e:
        print(f"Error al vaciar tablas: {e}")
        if conn: conn.rollback()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()

def populate_movies(manager):
    movies_to_add = [
        ("El Padrino", 175, "Crimen, Drama", "Francis Ford Coppola", "La épica saga de la familia Corleone y su imperio criminal en Nueva York."),
        ("Oppenheimer", 180, "Biografía, Drama, Historia", "Christopher Nolan", "La historia del científico J. Robert Oppenheimer y su papel en el desarrollo de la bomba atómica.")
    ]
    for title, duration, genre, director, synopsis in movies_to_add:
        if not manager.movie_repo.get_movie_by_title(title):
            manager.movie_repo.add_movie(title, duration, genre, director, synopsis)

def populate_rooms(manager):
    rooms_to_add = [("Sala Principal", 100), ("Sala 2", 75), ("Sala VIP", 30)]
    for name, capacity in rooms_to_add:
        if not manager.room_repo.get_room_by_name(name):
            manager.room_repo.add_room(name, capacity)

def populate_sessions_and_seats(manager):
    movies = manager.movie_repo.get_all_movies()
    rooms = manager.room_repo.get_all_rooms()

    if not movies or not rooms:
        return

    el_padrino_id = next((m['id'] for m in movies if m['title'] == 'El Padrino'), None)
    sala_principal_id = next((r['id'] for r in rooms if r['name'] == 'Sala Principal'), None)
    
    if el_padrino_id and sala_principal_id:
        today_date_str = datetime.now().strftime('%Y-%m-%d')
        manager.schedule_new_session(el_padrino_id, sala_principal_id, f"{today_date_str} 19:00:00", 8.50)

    for room in rooms:
        manager.seat_repo.create_seats_for_room(room['id'], room['capacity'])
from data_access.movie_repository import MovieRepository
from data_access.room_repository import RoomRepository
from data_access.session_repository import SessionRepository
from data_access.seat_repository import SeatRepository
from data_access.seat_reservation_repository import SeatReservationRepository
from datetime import datetime, timedelta
import re

class CinemaManager:
    def __init__(self):
        self.movie_repo = MovieRepository()
        self.room_repo = RoomRepository()
        self.session_repo = SessionRepository()
        self.seat_repo = SeatRepository()
        self.seat_reservation_repo = SeatReservationRepository()

    def get_available_movies(self):
        return self.movie_repo.get_all_movies()

    def get_all_sessions_details(self):
        return self.session_repo.get_all_sessions()

    def get_room_seats(self, room_id):
        return self.seat_repo.get_seats_by_room_id(room_id)

    def schedule_new_session(self, movie_id, room_id, start_time_str, price):
        movie = self.movie_repo.get_movie_by_id(movie_id)
        room = self.room_repo.get_room_by_id(room_id)

        if not movie:
            print(f"Error: La película con ID {movie_id} no existe.")
            return None
        if not room:
            print(f"Error: La sala con ID {room_id} no existe.")
            return None
        
        movie_duration_minutes = movie.get('duration_minutes')
        if not movie_duration_minutes:
            print(f"Error: La película con ID {movie_id} no tiene una duración válida.")
            return None
            
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = start_time + timedelta(minutes=movie_duration_minutes)
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

        all_sessions_for_room = self.session_repo.get_sessions_by_room_id(room_id)
        
        for session in all_sessions_for_room:
            existing_start = session['start_time']
            existing_end = session['end_time']
            
            if not (end_time <= existing_start or start_time >= existing_end):
                print(f"Error: La sala {room_id} está ocupada por la sesión ID {session['id']} "
                      f"en el horario {existing_start} a {existing_end}.")
                return None
        
        session_id = self.session_repo.add_session(movie_id, room_id, start_time_str, end_time_str, price)

        if session_id:
            print(f"Sesión agendada con éxito. ID: {session_id}, Película: '{movie['title']}' en Sala '{room['name']}'")
            return session_id
        else:
            print("Error desconocido al agendar la sesión.")
            return None

    def book_seat(self, session_id, seat_name):
        session = self.session_repo.get_session_by_id(session_id)
        if not session:
            print("Error: La sesión no existe.")
            return None

        seat_id = self.seat_repo.get_seat_by_name_and_room_id(seat_name, session['room_id'])
        if not seat_id:
            print(f"Error: El asiento '{seat_name}' no existe en la sala de la sesión {session_id}.")
            return None

        reservation_id = self.seat_reservation_repo.add_seat_reservation(session_id, seat_id)

        if reservation_id:
            print(f"¡Reserva exitosa! ID de reserva: {reservation_id} para el asiento {seat_name}.")
            return reservation_id
        else:
            print("No se pudo completar la reserva. El asiento podría ya estar ocupado.")
            return None
        
    def get_session_seat_status(self, session_id):
        session_details = self.session_repo.get_session_by_id(session_id)
        if not session_details:
            print(f"Error: La sesión con ID {session_id} no existe.")
            return None

        room_id = session_details.get('room_id')
        all_seats = self.seat_repo.get_seats_by_room_id(room_id)

        import re
        def sort_seats(seat):
            match = re.match(r"([A-Z]+)(\d+)", seat['seat_name'])
            if match:
                letter_part = match.group(1)
                number_part = int(match.group(2))
                return (letter_part, number_part)
            return (seat['seat_name'], 0)
        
        all_seats.sort(key=sort_seats)

        reserved_seat_ids = self.seat_reservation_repo.get_reserved_seats_for_session(session_id)

        seat_status = []
        for seat in all_seats:
            status = 'Reservado' if seat['id'] in reserved_seat_ids else 'Disponible'
            seat_status.append({
                'seat_id': seat['id'],
                'seat_name': seat['seat_name'],
                'status': status
            })
        
        session_details['seats'] = seat_status
        return session_details
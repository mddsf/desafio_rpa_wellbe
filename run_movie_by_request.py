from src.movie_challenge.movie_requests import RpaChallengeRequest
from src.services.db_service import add_movies

def main_movies(movie_name = "avengers"):
    rc_request = RpaChallengeRequest()
    if not rc_request.start_session():
        raise Exception(rc_request.error_message)
    
    if not rc_request.movie_search(movie_name):
        raise Exception(rc_request.error_message)
    
    if not rc_request.movies:
        print(f"Nenhum filme encontrado por '{movie_name}'")
    else:
        add_movies(rc_request.movies)

if __name__ == "__main__":
    main_movies()

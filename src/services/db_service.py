from src.database import get_session
from src.models import Movie, MovieSummary

def add_movies(movies: list[dict]):
    with get_session() as session:
        for item in movies:
            
            genre_ids_str = ",".join(str(gid) for gid in item["genre_ids"]) 
            genre_ids_str += ","

            if not session.get(Movie, item["id"]):
                movie = Movie(
                    id=item["id"],
                    title=item["title"],
                    original_title=item["original_title"],
                    original_language=item["original_language"],
                    overview=item.get("overview"),
                    popularity=item["popularity"],
                    poster_path=item.get("poster_path"),
                    backdrop_path=item.get("backdrop_path"),
                    release_date=item.get("release_date") or None,
                    adult=item["adult"],
                    video=item["video"],
                    vote_average=item["vote_average"],
                    vote_count=item["vote_count"],
                    genre_ids=genre_ids_str
                )
                session.add(movie)

        session.commit()


def add_movies_selenium(movies: list[dict]):
    with get_session() as session:
        for item in movies:
            exists = session.query(MovieSummary).filter_by(
                title=item["title"],
                description=item["description"],
            ).first()
            if not exists:
                movie = MovieSummary(
                    title=item["title"],
                    description=item["description"],
                )
                session.add(movie)

        session.commit()
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, Text, DateTime,
    ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id                = Column(Integer, primary_key=True)
    adult             = Column(Boolean)
    backdrop_path     = Column(String(255), nullable=True)
    genre_ids         = Column(String(255))
    original_language = Column(String(10))
    original_title    = Column(String(255))
    title             = Column(String(255))
    overview          = Column(Text)
    popularity        = Column(Float)
    poster_path       = Column(String(255), nullable=True)
    release_date      = Column(Date)
    video             = Column(Boolean)
    vote_average      = Column(Float)
    vote_count        = Column(Integer)
    created_at        = Column(DateTime, server_default=func.now())

class MovieSummary(Base):
    __tablename__ = "movies_summary"
    id    = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("title", "description", name="uq_title_description"),
    )

""" class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)

class MovieGenre(Base):
    __tablename__ = "movies_genre"
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genre.id"), primary_key=True)

    __table_args__ = (
        UniqueConstraint("movie_id", "genre_id", name="uq_movie_genre"),
    ) """
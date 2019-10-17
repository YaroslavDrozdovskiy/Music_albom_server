import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# импорт библиотеки для работы с регулярными выражениями
import re

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Error(Exception):
    pass


class AlreadyExists(Error):
    pass


class Album(Base):

    __tablename__ = 'album'

    id = sa.Column(sa.Integer, primary_key=True)
    year = sa.Column(sa.Integer)
    artist = sa.Column(sa.Text)
    genre = sa.Column(sa.Text)
    album = sa.Column(sa.Text)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    sessions = sessionmaker(engine)

    return sessions()


def find(artist):
    session = connect_db()
    album_list = session.query(Album).filter(Album.artist == artist).all()

    return album_list


def save_data(year, artist, genre, album):
    session = connect_db()

    assert isinstance(year, int), "Incorrect date"
    assert isinstance(artist, str), "Incorrect artist"
    assert isinstance(genre, str), "Incorrect genre"
    assert isinstance(album, str), "Incorrect album"

    saved_album = session.query(Album).filter(
        Album.album == album, Album.artist == artist).first()
    if saved_album is not None:
        raise AlreadyExists(
            "Album already exists and has #{}".format(saved_album.id))

    current_album = Album(year=year, artist=artist, genre=genre, album=album)

    session.add(current_album)

    session.commit()

    return current_album

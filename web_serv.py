from bottle import route
from bottle import request
from bottle import HTTPError
from bottle import run

import albumdb


@route("/albums", method="GET")
def get_data_from_GET():
    artist = request.query.artist
    album_list = albumdb.find(artist)
    if album_list:
        album_names = "<br><hr>".join([album.album for album in album_list])
        result_text = f"По вашему запросу исполнителя <b>{artist}</b> найдены альбомы: <br><hr><b>{album_names}</b>."
    else:
        error_messege = "По вашему запросу не найдено исполнителей."
        result_text = HTTPError(404, error_messege)
    return result_text


@route("/albums/<list_>")
def album_list(list_):
    session = albumdb.connect_db()
    album_list = set(
        album.artist for album in session.query(albumdb.Album).all())
    result_text = "Полный список исполнителей в базе данных: "
    result_text += ", ".join(album_list)
    return result_text


@route("/albums", method="POST")
def get_data_from_POST():
    # получение данных веб-формы
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album = request.forms.get("album")
    # создание словаря с введенными данными

    # функция вернет True, если все параметры будут удовлетворять условиям валидности
    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома")

    try:
        new_album = albumdb.save_data(year, artist, genre, album)
    except AssertionError as err:
        result_text = HTTPError(400, str(err))
    except albumdb.AlreadyExists as err:
        result_text = HTTPError(409, str(err))
    else:
        print(
            f"Added new data to the album: {new_album.id}|{new_album.year}|{new_album.artist}|{new_album.genre}|{new_album.album}")
        result_text = f"Данные успешно сохранены! id: {new_album.id}"
    return result_text


if __name__ == '__main__':
    run(host='localhost', port='8000', debug='true')

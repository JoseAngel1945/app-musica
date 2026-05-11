from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import artists, albums, songs, media, health

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Music App API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(songs.router)
app.include_router(media.router)
app.include_router(health.router)


@app.get("/search")
def global_search(q: str, db):
    from sqlalchemy.orm import Session
    from app.database import get_db
    from app.models.artist import Artist
    from app.models.album import Album
    from app.models.song import Song
    from sqlalchemy import or_

    session: Session = next(get_db())
    artists_result = session.query(Artist).filter(Artist.name.ilike(f"%{q}%")).limit(5).all()
    albums_result = session.query(Album).filter(Album.title.ilike(f"%{q}%")).limit(5).all()
    songs_result = session.query(Song).filter(Song.title.ilike(f"%{q}%")).limit(10).all()

    artist_list = [{"id": a.id, "name": a.name, "image_path": a.image_path} for a in artists_result]
    album_list = []
    for a in albums_result:
        artist = session.query(Artist).filter(Artist.id == a.artist_id).first()
        album_list.append({"id": a.id, "title": a.title, "cover_path": a.cover_path, "artist_name": artist.name if artist else None})
    song_list = []
    for s in songs_result:
        artist = session.query(Artist).filter(Artist.id == s.artist_id).first()
        album = session.query(Album).filter(Album.id == s.album_id).first()
        song_list.append({"id": s.id, "title": s.title, "duration": s.duration, "artist_name": artist.name if artist else None, "album_title": album.title if album else None, "cover_path": album.cover_path if album else None})

    return {"artists": artist_list, "albums": album_list, "songs": song_list}


@app.get("/genres")
def list_genres():
    from sqlalchemy.orm import Session
    from app.database import get_db
    from app.models.genre import Genre
    session: Session = next(get_db())
    genres = session.query(Genre).order_by(Genre.name).all()
    return [{"id": g.id, "name": g.name} for g in genres]

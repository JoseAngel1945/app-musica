# Music App

Music streaming app estilo Spotify.

## Stack
- **Backend:** Python 3.12+ / FastAPI / SQLite / SQLAlchemy
- **Mobile:** Kotlin / Jetpack Compose / Room / ExoPlayer (Media3) / Retrofit

## Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Mobile Setup
Abrir `mobile/` en Android Studio y Run.

## Seed data
```bash
python app/seed.py seed_data.json
```
# DOKUMENTACJA PROJEKTU
## AI Age Recognition - System Rozpoznawania Wieku

**Status projektu:** W fazie rozwoju (40% ukończenia)
**Data:** Październik 2025

---

## 1. INFORMACJE PODSTAWOWE

### Cel projektu
Aplikacja webowa wykorzystująca sztuczną inteligencję do automatycznej predykcji wieku osób na podstawie analizy zdjęć twarzy. System oferuje alternatywną metodę weryfikacji wieku przez użycie kamery zamiast ręcznego wprowadzania danych.

### Technologie
**Backend:**
- Python 3.x + FastAPI
- SQLAlchemy ORM + SQLite
- JWT (planowane) do autoryzacji
- SHA-256 do haszowania haseł (planowane: bcrypt)

**AI/ML (planowane):**
- OpenCV - detekcja twarzy
- TensorFlow/PyTorch - predykcja wieku
- NumPy, Pillow - przetwarzanie obrazów

**Frontend (planowane):**
- HTML5, CSS3, JavaScript
- WebRTC - dostęp do kamery

---

## 2. STRUKTURA PROJEKTU

```
AI_Age_Recognition/
├── backend/
│   ├── app.py                    # Główna aplikacja FastAPI
│   ├── config.py                 # Konfiguracja (JWT, DB)
│   ├── database/
│   │   ├── database.py           # SQLAlchemy setup
│   │   ├── models.py             # Modele ORM (User)
│   │   ├── schema.sql            # Schema SQL
│   │   └── ai_age_recognition.db # Baza SQLite
│   ├── routes/
│   │   ├── auth_routes.py        # /signup, /login
│   │   └── ai_routes.py          # /getAge
│   ├── models/
│   │   └── age_model.py          # Model AI (TODO)
│   ├── services/
│   │   ├── image_preprocessing.py
│   │   └── camera_service.py
│   └── utils/
│       └── password_hashing.py   # SHA-256
├── frontend/
│   ├── templates/                # HTML (TODO)
│   └── static/                   # CSS, JS (TODO)
├── data/
│   ├── dataset/                  # Dane treningowe
│   └── uploads/                  # Przesłane zdjęcia
└── main.py                       # Punkt wejścia
```

---

## 3. BAZA DANYCH

**SQLite** - 3 tabele:

### Users
```sql
CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Predictions
```sql
CREATE TABLE Predictions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES Users(id) ON DELETE CASCADE,
    image_path VARCHAR(255),
    predicted_age INTEGER,
    confidence DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sessions
```sql
CREATE TABLE Sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES Users(id) ON DELETE CASCADE,
    token VARCHAR(512) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);
```

**Relacje:** CASCADE DELETE - usunięcie użytkownika usuwa jego predykcje i sesje.

---

## 4. API ENDPOINTS

### POST /signup
**Rejestracja użytkownika**

Request:
```json
{
    "username": "jan_kowalski",
    "password": "haslo123"
}
```

Response (sukces):
```json
{
    "status": "ok",
    "message": "User created successfully"
}
```

Response (błąd):
```json
{
    "status": "error",
    "message": "Username already exists"
}
```

---

### POST /login
**Logowanie użytkownika**

Request:
```json
{
    "username": "jan_kowalski",
    "password": "haslo123"
}
```

Response (sukces):
```json
{
    "status": "ok",
    "message": "Login successful"
}
```

**TODO:** Zwracanie tokenu JWT

---

### POST /getAge
**Predykcja wieku na podstawie zdjęcia**

Request (multipart/form-data):
- `user_id`: integer
- `file`: zdjęcie (JPG/PNG)

Response:
```json
{
    "user_id": 1,
    "predicted_age": 25,
    "confidence": 0.92,
    "image_path": "data/uploads/uuid.jpg"
}
```

**Aktualny status:** Endpoint działa, ale AI model jest placeholderem (zwraca stałe wartości).

---

### GET /health
**Sprawdzenie statusu API**

Response:
```json
{
    "status": "ok",
    "message": "API is running"
}
```

---

## 5. INSTALACJA I URUCHOMIENIE

### Wymagania
- Python 3.8+
- 4 GB RAM (8 GB dla ML)

### Instalacja
```bash
# Klonowanie repo
git clone https://github.com/your-username/AI_Age_Recognition.git
cd AI_Age_Recognition

# Wirtualne środowisko
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalacja zależności
pip install fastapi uvicorn sqlalchemy pydantic python-multipart
```

### Uruchomienie
```bash
# Metoda 1: Bezpośrednio
python main.py

# Metoda 2: Uvicorn z hot-reload
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

**Dostęp:**
- API: http://localhost:8000
- Dokumentacja Swagger: http://localhost:8000/docs
- Health check: http://localhost:8000/health

---

## 6. TESTOWANIE API

### cURL
```bash
# Signup
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "pass123"}'

# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "pass123"}'

# Predykcja wieku
curl -X POST http://localhost:8000/getAge \
  -F "user_id=1" \
  -F "file=@photo.jpg"
```

---

## 7. STATUS IMPLEMENTACJI

### ✅ UKOŃCZONE
- Struktura projektu i organizacja plików
- FastAPI setup z CORS
- Baza danych SQLite (schemat + inicjalizacja)
- Modele SQLAlchemy
- Endpointy: `/signup`, `/login`, `/getAge`, `/health`
- Haszowanie haseł (SHA-256)
- Zapis przesłanych obrazów (UUID)
- Zapis predykcji do bazy

### ⏳ W TRAKCIE / TODO
**Backend:**
- [ ] JWT - generowanie i weryfikacja tokenów
- [ ] Middleware uwierzytelniania
- [ ] Model AI predykcji wieku
- [ ] Detekcja twarzy (OpenCV)
- [ ] Przetwarzanie obrazów
- [ ] System logowania (logger)

**Frontend:**
- [ ] Strona główna (index.html)
- [ ] Formularz login/signup
- [ ] Panel użytkownika (dashboard)
- [ ] Interfejs kamery (WebRTC)
- [ ] Wyświetlanie wyników predykcji
- [ ] CSS stylizacja

**Bezpieczeństwo:**
- [ ] Zmiana SHA-256 na bcrypt
- [ ] Dodanie salt do haseł
- [ ] Rate limiting
- [ ] Walidacja inputów

---

## 8. ZNANE PROBLEMY

### Bezpieczeństwo
1. **SHA-256 bez salt** - podatne na rainbow table attacks → **Rozwiązanie:** bcrypt
2. **Brak JWT** - login nie zwraca tokenu → **Rozwiązanie:** implementacja PyJWT
3. **Hardcoded SECRET_KEY** w config.py → **Rozwiązanie:** zmienne środowiskowe

### Funkcjonalność
4. **Model AI placeholder** - zwraca stałe wartości (age=25) → **Rozwiązanie:** trening modelu
5. **Brak detekcji twarzy** - akceptuje dowolny obraz → **Rozwiązanie:** OpenCV
6. **Pusty frontend** - brak UI → **Rozwiązanie:** HTML/CSS/JS

### Infrastruktura
7. **SQLite w produkcji** - problemy z concurrency → **Rozwiązanie:** PostgreSQL

---

## 9. PLAN DALSZEGO ROZWOJU

### Priorytet 1 (1-2 tygodnie)
1. **Bezpieczeństwo** - implementacja bcrypt + JWT
2. **Podstawowy frontend** - formularz login/signup + upload zdjęć
3. **Testy** - pytest dla endpointów

### Priorytet 2 (1-2 miesiące)
4. **Model AI** - trening na UTKFace dataset
5. **Detekcja twarzy** - OpenCV Haar Cascade
6. **Frontend kamery** - WebRTC

### Priorytet 3 (3-6 miesięcy)
7. **Skalowanie** - Docker + PostgreSQL + Cloud deployment
8. **Monitoring** - Prometheus + Grafana
9. **Rozszerzenia** - detekcja emocji, płci, wiele twarzy

---

## 10. PRZYKŁAD IMPLEMENTACJI AI

### Model predykcji wieku (planowany)
```python
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout

def create_age_model():
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation='linear')(x)  # Regression

    model = tf.keras.Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer='adam', loss='mae', metrics=['mae'])

    return model
```

### Detekcja twarzy (planowana)
```python
import cv2

def detect_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    return faces[0] if len(faces) > 0 else None
```

---

## 11. ŹRÓDŁA

**Dokumentacja:**
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- OpenCV: https://docs.opencv.org/

**Datasets:**
- UTKFace: https://susanqq.github.io/UTKFace/
- IMDB-WIKI: https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/

**Bezpieczeństwo:**
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Passlib: https://passlib.readthedocs.io/

---

**KONIEC DOKUMENTACJI**

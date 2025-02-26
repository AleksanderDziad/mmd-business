# ✅ Użycie lekkiej wersji Pythona
FROM python:3.10-slim

# ✅ Ustawienie katalogu roboczego
WORKDIR /app

# ✅ Instalacja zależności systemowych dla PostgreSQL i `psycopg2`
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ✅ Ustawienie zmiennej środowiskowej PYTHONPATH
ENV PYTHONPATH="/app"

# ✅ Kopiowanie pliku zależności
COPY requirements.txt /app/requirements.txt

# ✅ Instalacja zależności Pythona
RUN pip install --no-cache-dir --upgrade pip && \
    if [ -f /app/requirements.txt ]; then pip install --no-cache-dir -r /app/requirements.txt; fi

# ✅ Kopiowanie całej aplikacji do katalogu roboczego w kontenerze
COPY ./app /app/

# ✅ Otworzenie portu aplikacji
EXPOSE 8000

# ✅ Uruchomienie aplikacji FastAPI
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]


# Używamy stabilnej wersji Pythona
FROM python:3.10

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy najpierw requirements.txt (lepszy cache)
COPY requirements.txt .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Teraz kopiujemy kod aplikacji
COPY . .

# Eksponujemy port
EXPOSE 5000

# Uruchamiamy aplikację Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


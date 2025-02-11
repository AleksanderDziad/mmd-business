FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask flask_sqlalchemy psycopg2-binary flask-migrate flask-jwt-extended
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

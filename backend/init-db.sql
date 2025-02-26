-- Tworzenie użytkownika, jeśli nie istnieje
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'db_user') THEN
        CREATE USER db_user WITH ENCRYPTED PASSWORD 'db_password';
    END IF;
END $$;

-- Tworzenie bazy danych, jeśli nie istnieje
CREATE DATABASE db_user OWNER db_user;


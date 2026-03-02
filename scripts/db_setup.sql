
DROP DATABASE IF EXISTS portafolio_modulo8 ;
CREATE DATABASE portafolio_modulo8 ;
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE portafolio_modulo8 TO postgres;
SET default_tablespace = krankenhausspace;

CREATE TABLE IF NOT EXISTS krankenhaus (
    id                  INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    version             INTEGER NOT NULL DEFAULT 0,
    name                TEXT NOT NULL,
    mitarbeiteranzahl   INTEGER,
    bettenanzahl        INTEGER,
    email               TEXT NOT NULL UNIQUE,
    telefonnummer       TEXT NOT NULL UNIQUE,
    erzeugt             TIMESTAMP NOT NULL,
    aktualisiert        TIMESTAMP NOT NULL
)

CREATE INDEX IF NOT EXISTS krankenhaus_name_idx ON krankenhaus(name);

CREATE TABLE IF NOT EXISTS adresse (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    strasse         TEXT NOT NULL,
    hausnummer      TEXT NOT NULL,
    plz             TEXT NOT NULL CHECK (plz ~ '\d{5}'),
    ort             TEXT NOT NULL,
    krankenhaus_id  INTEGER NOT NULL REFERENCES krankenhaus ON DELETE CASCADE
)

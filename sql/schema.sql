-- Schéma Oracle (XE) utilisé par le projet.
-- À exécuter avec un compte administrateur, puis adapter le mot de passe.

CREATE USER pro IDENTIFIED BY "CHANGER_CE_MOT_DE_PASSE"
  DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
GRANT CREATE SESSION TO pro;

-- Mesures brutes reçues depuis la carte STM32 (voir rapport, figure 21)
CREATE TABLE pro.capteur (
    temp  NUMBER,
    hum   NUMBER,
    dates TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP
);

-- Historique des alertes écrit par l'interface Qt
CREATE TABLE pro.temp (
    temp   NUMBER,
    hum    NUMBER,
    limite NUMBER,
    etat   VARCHAR2(10)
);

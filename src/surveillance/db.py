"""Connexion à la base Oracle."""
import oracledb

from . import config


def connect():
    """Retourne une connexion Oracle configurée via l'environnement."""
    if not config.DB_PASSWORD:
        raise RuntimeError(
            "DB_PASSWORD manquant : copiez .env.example vers .env et renseignez-le."
        )
    dsn = oracledb.makedsn(config.DB_HOST, config.DB_PORT, service_name=config.DB_SERVICE)
    return oracledb.connect(user=config.DB_USER, password=config.DB_PASSWORD, dsn=dsn)

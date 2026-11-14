"""Lit les mesures envoyées par la carte STM32 et les enregistre dans Oracle.

Format de ligne attendu : ``TEMP:23.5;HUM:48.2``
Usage : ``python -m surveillance.serial_reader``
"""
import oracledb
import serial

from . import config, db

INSERT_SQL = "INSERT INTO capteur (temp, hum) VALUES (:1, :2)"


def parse_line(line):
    """Retourne (temp, hum) ou None si la ligne n'est pas une mesure valide."""
    if "TEMP" not in line:
        return None
    try:
        temp_part, hum_part = line.split(";")[:2]
        return float(temp_part.split(":")[1]), float(hum_part.split(":")[1])
    except (ValueError, IndexError):
        return None


def main():
    ser = serial.Serial(config.SERIAL_PORT, config.SERIAL_BAUDRATE, timeout=1)
    conn = db.connect()
    print("Réception en temps réel... (Ctrl+C pour arrêter)")
    try:
        with conn.cursor() as cur:
            while True:
                line = ser.readline().decode(errors="ignore").strip()
                if not line:
                    continue
                values = parse_line(line)
                if values is None:
                    print(line)
                    continue
                temp, hum = values
                print(f"Température : {temp} °C | Humidité : {hum} %")
                try:
                    cur.execute(INSERT_SQL, values)
                    conn.commit()
                except oracledb.DatabaseError as exc:
                    (error,) = exc.args
                    print(f"Erreur Oracle {error.code} : {error.message}")
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        conn.close()


if __name__ == "__main__":
    main()

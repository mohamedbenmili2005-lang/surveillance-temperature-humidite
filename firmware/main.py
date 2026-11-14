"""Firmware MicroPython pour carte STM32 NUCLEO-F401RE + capteur DHT22.

Reconstitué à partir de la figure 17 du rapport de stage.
À copier sur la carte sous le nom ``main.py`` (via Thonny) : il est exécuté
automatiquement au démarrage.

Câblage DHT22 : VCC -> 3,3 V | DATA -> broche D5 (PB4 selon la carte, voir
``Pin`` ci-dessous) | GND -> GND.
"""
from machine import Pin
import dht
import time

# Adapter le nom de la broche à votre câblage (D5 dans le rapport).
sensor = dht.DHT22(Pin('D5'))

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        # Format attendu par le lecteur série : TEMP:<valeur>;HUM:<valeur>
        print(f"TEMP:{temp};HUM:{hum}")
        time.sleep(2)
    except Exception:
        print("ERREUR_CAPTEUR")
        time.sleep(2)

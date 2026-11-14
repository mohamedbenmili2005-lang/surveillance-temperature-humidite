"""Interface web Flask : tableau des mesures.

Usage : ``python -m surveillance.web_app.app``
"""
from flask import Flask, jsonify, render_template

from .. import config, db

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data")
def get_data():
    conn = db.connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT temp, hum, dates FROM capteur ORDER BY dates")
            rows = cur.fetchall()
    finally:
        conn.close()
    return jsonify([{"temp": t, "hum": h, "dates": d} for t, h, d in rows])


if __name__ == "__main__":
    app.run(host=config.WEB_HOST, port=config.WEB_PORT)

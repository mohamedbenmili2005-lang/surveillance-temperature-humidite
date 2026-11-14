"""Interface PyQt5 : affichage en direct, seuil d'alerte et historique.

Usage : ``python -m surveillance.qt_app.app``
"""
import sys
from pathlib import Path

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

from .. import db

UI_FILE = Path(__file__).with_name("interface.ui")
INSERT_SQL = "INSERT INTO temp (temp, hum, limite, etat) VALUES (:1, :2, :3, :4)"


class MainWindow:
    def __init__(self):
        self.conn = db.connect()
        self.w = loadUi(str(UI_FILE))
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.w.d.clicked.connect(self.start)
        self.w.ar.clicked.connect(self.timer.stop)

    def start(self):
        self.timer.start(int(self.w.refresh.text()) * 1000)

    def refresh(self):
        limite = int(self.w.limite.text())
        with self.conn.cursor() as cur:
            cur.execute("SELECT temp, hum, dates FROM capteur ORDER BY dates")
            rows = cur.fetchall()
            self.w.a.setRowCount(0)
            alert = False
            for i, (temp, hum, dates) in enumerate(rows):
                etat = "Alert" if temp > limite else "Stable"
                alert = alert or etat == "Alert"
                self.w.a.insertRow(i)
                for col, value in enumerate((temp, hum, dates, etat)):
                    self.w.a.setItem(i, col, QTableWidgetItem(str(value)))
            if rows:
                temp, hum, _ = rows[-1]
                self.w.temp.display(temp)
                self.w.h.display(hum)
                cur.execute(INSERT_SQL, (temp, hum, limite, "alert" if temp > limite else "stable"))
                self.conn.commit()
        self.w.a.scrollToBottom()
        if alert:
            self.timer.stop()
            QMessageBox.warning(self.w, "Alerte", "Température au-dessus du seuil !")

    def show(self):
        self.w.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

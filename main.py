import sys
import requests

from PyQt5.Qt import QMainWindow, QApplication
from PyQt5 import uic
from io import BytesIO
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap


class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/map-ui.ui", self)
        self.setFixedSize(700, 500)

        self.pushButton.clicked.connect(self.show_map)

        self.server = "http://static-maps.yandex.ru/1.x/"

    def show_map(self):
        is_coords_right = True
        try:
            coords = [float(self.lineEdit.text()), float(self.lineEdit_2.text())]
        except:
            self.statusBar().showMessage("Неверный формат координат", 3000)
            is_coords_right = False

        if is_coords_right:
            map_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "ll": ",".join([str(i) for i in coords]),
                "l": "map",
                "spn": ",".join([str(i) for i in [0.01, 0.01]]),
                "size": ",".join([str(i) for i in [450, 450]])
            }
            response = requests.get(self.server, params=map_params)
            if response:
                map = Image.open(BytesIO(response.content))
                qimg = ImageQt(map)
                pixmap = QPixmap.fromImage(qimg)
                self.label_4.setPixmap(pixmap)
            else:
                self.statusBar().showMessage(f"Ошибка {str(response.status_code)}", 3000)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = AppMainWindow()
    main_window.show()
    app.exec()

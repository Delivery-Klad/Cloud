from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import numpy
import sys


class Gears(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(510, 510)
        self._qpainter = QtGui.QPainter()
        self.rotate = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(33)

    def update_values(self):
        self.rotate += 1
        self.update()

    def paintEvent(self, event):
        self.draw_hours()
        self.draw_gear(radius=65, coef=60, g=128)
        self.draw_gear(radius=25, coef=0.25, rev=False, b=205)
        self.draw_gear(r=255, g=165)
        self.draw_gear(x=200, y=280, rev=False, g=139, b=139)
        self.draw_gear(x=235, y=340, r=139)
        self.draw_gear(x=298, y=368, rev=False, b=205)
        self.draw_arrow(radius=3600)
        self.draw_arrow(radius=300)
        self.draw_arrow(radius=5)

    def draw_hours(self):
        """
        Отрисовка часовых точек
        :return:
        """
        _qpainter = QtGui.QPainter()
        _qpainter.begin(self)
        _qpainter.setRenderHint(QtGui.QPainter.Antialiasing)
        _qpainter.setTransform(QtGui.QTransform(1, 0, 0, 1, 255, 240))
        _qpainter.setPen(QtGui.QColor(0, 0, 0, 0))
        _qpainter.setBrush(QtGui.QColor(0, 0, 0))
        for alpha in range(0, 360, 30):
            x = 210 * numpy.cos(numpy.radians(alpha) - numpy.pi / 2)
            y = 210 * numpy.sin(numpy.radians(alpha) - numpy.pi / 2)
            _qpainter.drawEllipse(x - 10 / 2, y - 10 / 2, 10, 10)

    def draw_arrow(self, radius):
        """
        Отрисовка стрелок часов
        :param radius:
        :return:
        """
        color = 100 if radius == 3600 else 50 if radius == 300 else 0
        transform = QtGui.QTransform(1, 0, 0, 1, 255, 240)
        transform.rotate((100 / radius) * self.rotate)
        _qpainter = QtGui.QPainter()
        _qpainter.begin(self)
        _qpainter.setRenderHint(QtGui.QPainter.Antialiasing)
        _qpainter.setTransform(transform)
        _qpainter.setPen(QtGui.QColor(0, 0, 0, 0))
        _qpainter.setBrush(QtGui.QColor(color, color, color))
        _qpainter.drawRect(int(5 / -2), 0, 5, -(110 if radius == 3600 else 150 if radius == 300 else 200))
        _qpainter.end()

    def draw_gear(self, r=0, g=0, b=0, x=255, y=240, radius=40, coef=7.5, rev=True):
        """
        Отрисочвка шестерней
        :param r: r цвет
        :param g: g цвет
        :param b: b цвет
        :param x: x координата центра
        :param y: y координата центра
        :param radius: радиус
        :param coef: коофициент вращения
        :param rev: реверс
        :return:
        """
        triangls = []
        for i in range(15):
            triangls.append([radius * 3 / 4 * numpy.cos(i * 2 * numpy.pi / 15),
                             radius * 3 / 4 * numpy.sin(i * 2 * numpy.pi / 15)]),
            triangls.append([radius * numpy.cos(i * 2 * numpy.pi / 15 + numpy.pi / 15),
                             radius * numpy.sin(i * 2 * numpy.pi / 15 + numpy.pi / 15)]),
        triangls.sort(key=lambda c: numpy.arctan2(c[0], c[1]), reverse=rev)

        transform = QtGui.QTransform(1, 0, 0, 1, x, y)
        transform.rotate(100 / (radius * coef) * self.rotate * (1 if rev else -1))
        _qpainter = QtGui.QPainter()
        _qpainter.begin(self)
        _qpainter.setRenderHint(QtGui.QPainter.Antialiasing)
        _qpainter.setTransform(transform)
        path = QtGui.QPainterPath()
        path.clear()
        for i in triangls:
            path.lineTo(i[0], i[1])
        path.lineTo(triangls[0][0], triangls[0][1])
        path.addEllipse(radius * -0.6, radius * -0.6, radius * 1.2, radius * 1.2)
        _qpainter.fillPath(path, QtGui.QBrush(QtGui.QColor(r, g, b)))

        path.clear()
        path.setFillRule(QtCore.Qt.WindingFill)
        path.addRect(radius / -8, radius / -1.6, radius / 4, radius * 1.3)
        path.addRect(radius / -1.6, radius / -8, radius * 1.3, radius / 4)
        path.addEllipse(radius / -4, radius / -4, radius / 2, radius / 2)
        _qpainter.fillPath(path, QtGui.QBrush(QtGui.QColor(r, g, b)))


app = QtWidgets.QApplication(sys.argv)
window = Gears()
window.show()
window.setWindowTitle("Валяев Д.А. ИКБО-08-18")
app.exec()

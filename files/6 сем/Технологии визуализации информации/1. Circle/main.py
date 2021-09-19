from PyQt5 import QtWidgets, QtGui
import sys
import numpy


class Circle(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.h = 0
        self.radius_in, self.radius_out = 160, 220
        a, b = self.radius_in * numpy.sin(numpy.deg2rad(30)), self.radius_in * numpy.cos(numpy.deg2rad(30))
        self.triangle_a = (2 * (self.radius_in + a)) / numpy.sqrt(3)
        self.ax, self.ay = self.radius_out + a, self.radius_out - b
        self.bx, self.by = self.radius_out - self.radius_in, self.radius_out
        self.cx, self.cy = self.radius_out + a, self.radius_out + b
        palette = QtGui.QPalette()
        self.setPalette(palette)
        self.setFixedSize(self.radius_out * 2, self.radius_out * 2)

    def set_triangle(self):
        try:
            h = self.h * 360
            self.by = self.radius_out + self.radius_in * numpy.cos(numpy.radians(h) - numpy.pi / 2)
            self.bx = self.radius_out + self.radius_in * numpy.sin(numpy.radians(h) - numpy.pi / 2)
            self.ay = self.radius_out + self.radius_in * numpy.cos(numpy.radians(h + 120 if h + 120 <= 360 else h - 240)
                                                                   - numpy.pi / 2)
            self.ax = self.radius_out + self.radius_in * numpy.sin(numpy.radians(h + 120 if h + 120 <= 360 else h - 240)
                                                                   - numpy.pi / 2)
            self.cy = self.radius_out + self.radius_in * numpy.cos(numpy.radians(h - 120 if h - 120 >= 0 else h + 240)
                                                                   - numpy.pi / 2)
            self.cx = self.radius_out + self.radius_in * numpy.sin(numpy.radians(h - 120 if h - 120 >= 0 else h + 240)
                                                                   - numpy.pi / 2)
        except Exception as er:
            print(er)

    def entry_circle(self, x, y):
        try:
            a = numpy.sqrt(numpy.power(y - self.radius_out, 2) + numpy.power(x - self.radius_out, 2)) / self.radius_out
            if self.radius_out / self.radius_out >= a >= self.radius_in / self.radius_out:
                b = 1 - (numpy.arctan2(y - self.radius_out, x - self.radius_out) + numpy.pi) / (2. * numpy.pi)
                return a, b
        except Exception as er:
            print(er)

    def entry_triangle(self, x, y):
        try:
            bx, by = self.bx - self.ax, self.by - self.ay
            cx, cy = self.cx - self.ax, self.cy - self.ay
            dx, dy = x - self.ax, y - self.ay
            temp = (dx * by - bx * dy) / (cx * by - bx * cy)
            if 0 < temp < 1:
                i = (dx - temp * cx) / bx
                if 0 < i and temp + i < 1:
                    a = numpy.sqrt((self.ax - x) ** 2 + (self.ay - y) ** 2) / self.triangle_a
                    b = numpy.sqrt((self.cx - x) ** 2 + (self.cy - y) ** 2) / self.triangle_a
                    return a, b
        except Exception as er:
            print(er)

    def paintEvent(self, event):
        try:
            super().paintEvent(event)
            self.draw_circle()
            self.draw_triangle()
        except Exception as er:
            print(er)

    def mousePressEvent(self, event):
        try:
            super().mousePressEvent(event)
            x, y = event.y(), event.x()
            try:
                self.h = self.entry_circle(x, y)[1]
                self.set_triangle()
                self.update()
            except TypeError:
                try:
                    a, b = self.entry_triangle(x, y)
                    color = QtGui.QColor(255, 255, 255, 255)
                    color.setHsvF(self.h, b, a, 1)
                    QtWidgets.QMessageBox.about(self, 'Colors', f'RGB: {color.getRgb()}\n'
                                                                f'HSV: {color.getHsv()}\n'
                                                                f'Cmyk: {color.getCmyk()}')
                except Exception as error:
                    pass
                    # print(error)
        except Exception as er:
            print(er)

    def draw_circle(self):
        """
        Рисовалка кольца
        :return:
        """
        try:
            _qpainter = QtGui.QPainter(self)
            _qpainter.begin(self)
            _qpainter.setRenderHint(QtGui.QPainter.Antialiasing)
            for y in range(self.radius_out * 2):
                for x in range(self.radius_out * 2):
                    try:
                        a, b = self.entry_circle(x, y)
                        color = QtGui.QColor(255, 255, 255, 255)
                        color.setHsvF(b, a, 1, 1)
                        _qpainter.setPen(color)
                        _qpainter.drawPoint(y, x)
                    except Exception as error:
                        pass
                        # print(error)
            _qpainter.end()
        except Exception as er:
            print(er)

    def draw_triangle(self):
        """
        Рисовалка треугольника
        :return:
        """
        try:
            _qpainter = QtGui.QPainter(self)
            _qpainter.begin(self)
            _qpainter.setRenderHint(QtGui.QPainter.Antialiasing)
            for y in range(self.radius_out * 2):
                for x in range(self.radius_out * 2):
                    try:
                        a, b = self.entry_triangle(x, y)
                        color = QtGui.QColor(255, 255, 255, 255)
                        color.setHsvF(self.h, b, a, 1)
                        _qpainter.setPen(color)
                        _qpainter.drawPoint(y, x)
                    except Exception as error:
                        pass
                        # print(error)
            _qpainter.end()
        except Exception as er:
            print(er)


app = QtWidgets.QApplication(sys.argv)
window = Circle()
window.show()
window.setWindowTitle("Валяев Д.А. ИКБО-08-18")
app.exec()

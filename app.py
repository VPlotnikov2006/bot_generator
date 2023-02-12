import math
import random
import sys
import pyautogui

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMenuBar, QMenu, QFileDialog
from PyQt5.QtGui import QPainter, QPen
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QTimer


class ButtonConflictError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Drawing(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = QtWidgets.QWidget(self)
        self.box.setGeometry(0, 0, 500, 200)
        self.click = []

    def draw(self):
        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        for p in self.click:
            qp.drawPoint(p)
        qp.end()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if self.click:
            self.draw()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.click.append(a0.pos())
        self.update()


class Line(QWidget):
    def __init__(self, window,  size=QPoint(0, 0), pos1=QPoint(0, 0), pos2=QPoint(0, 0)):
        super().__init__(window)
        self.p1 = pos1
        self.p2 = pos2
        self.setGeometry(0, 0, size.x(), size.y())

    def set(self, p1, p2):
        self.p2 = p2
        self.p1 = p1

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if self.p1 and self.p2:

            qp = QPainter()
            qp.begin(self)
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(self.p1, self.p2)

            try:
                x1, y1 = self.p1.x(), self.p1.y()
                x2, y2 = self.p2.x(), self.p2.y()
                a = math.atan2(y1 - y2, x1 - x2)
                ln = 20
                da = math.radians(15)
                xd1, yd1 = x2 + round(ln * math.cos(a + da)), y2 + round(ln * math.sin(a + da))
                xd2, yd2 = x2 + round(ln * math.cos(a - da)), y2 + round(ln * math.sin(a - da))

                qp.drawLine(xd1, yd1, x2, y2)
                qp.drawLine(xd2, yd2, x2, y2)
            except Exception as e:
                print(e)
            qp.end()


class TapButton(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.f = []
        self.box = QtWidgets.QWidget(self)
        self.selected = False
        self.connect(self.select)

    def select(self):
        self.selected = not self.selected

    def connect(self, f, *args):
        self.f.append((f, args))

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        for func, args in self.f:
            func(*args)


class MovingButton(QWidget):
    def __init__(self, window, r, color='black', select_color='rgb(255, 0, 0)'):
        self.r = r
        self.select_color = select_color
        self.color = color
        self.pt = '''QWidget {{
                     border-style: solid; 
                     border-radius: {r}px; 
                     border-color: {color}; 
                     border-width: 2px;
                     background-color: {bg_color}; 
                 }}'''
        super().__init__(window)
        self.b2 = QtWidgets.QWidget(self)
        self.b2.setStyleSheet(self.pt.format(r=r//2, color=self.color, bg_color=self.color))
        self.b2.resize((r//2)*2, (r//2)*2)
        self.b2.move(r//2, r//2)
        self.button = TapButton(self)
        self.button.box.setStyleSheet(self.pt.format(r=r, color=self.color, bg_color='rgba(0,0,0,0)'))
        self.button.box.resize(2*r, 2*r)
        self.button.connect(self.set_start)
        self.sp = QPoint(*pyautogui.position())
        self.p = QPoint(0, 0)
        self.resize(2*r, 2*r)

    def set_pos(self, x, y):
        self.move(x - self.r, y - self.r)
        self.p = QPoint(x - self.r, y - self.r)

    def set_start(self):
        self.sp = QPoint(*pyautogui.position())

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if self.button.selected:
            self.button.box.setStyleSheet(self.pt.format(r=self.r, color=self.select_color, bg_color='rgba(0,0,0,0)'))
            self.b2.setStyleSheet(self.pt.format(r=self.r // 2, color=self.select_color, bg_color=self.select_color))
        else:
            self.button.box.setStyleSheet(self.pt.format(r=self.r, color=self.color, bg_color='rgba(0,0,0,0)'))
            self.b2.setStyleSheet(self.pt.format(r=self.r // 2, color=self.color, bg_color=self.color))

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.set_start()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.move(self.p + QPoint(*pyautogui.position()) - self.sp)
        self.button.box.setStyleSheet(self.pt.format(r=self.r, color=self.color, bg_color='rgba(0,0,0,0)'))
        self.b2.setStyleSheet(self.pt.format(r=self.r // 2, color=self.color, bg_color=self.color))
        self.button.selected = False

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.p += QPoint(*pyautogui.position()) - self.sp


class Graph(QWidget):
    def __init__(self, window, n, size):
        super().__init__(window)
        self.setGeometry(0, 0, size.x(), size.y())
        self.bg = QWidget(self)
        self.bg.setGeometry(0, 0, size.x(), size.y())
        self.adj_list = [[] for _ in range(n)]
        self.bt = [MovingButton(self, 10, 'black') for _ in range(n)]
        self.size = size
        self.n = n
        for i, b in enumerate(self.bt):
            b.button.connect(self.add_edje, i)
            b.button.connect(self.unselect, i)
            b.set_pos(random.randint(0, self.size.x()), random.randint(0, self.size.y()))
        self.selected = None
        self.lns = [[Line(self.bg, size) for _ in range(n)] for _ in range(n)]
        t = QTimer(self)
        t.timeout.connect(self.update)
        t.timeout.connect(self.update_lns)
        t.setInterval(10)
        t.start()

    def button_click(self, bt_id):
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.selected = None
        for i, b in enumerate(self.bt):
            if self.selected is not None and b.button.selected:
                raise ButtonConflictError('conflict')
            if b.button.selected:
                self.selected = i

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        try:
            for b in self.bt:
                b.button.selected = False
        except Exception as e:
            print(e)

    def unselect(self, bt_id):
        for i, b in enumerate(self.bt):
            if i == bt_id:
                continue
            b.button.selected = False

    def update_lns(self):
        for i, l in enumerate(self.adj_list):
            for j in l:
                self.lns[i][j].set(self.bt[i].p + QPoint(self.bt[i].r, self.bt[i].r),
                                   self.bt[j].p + QPoint(self.bt[i].r, self.bt[i].r))

    def add_edje(self, bt_id):
        if self.selected is None:
            return
        if self.selected == bt_id:
            return
        if bt_id in self.adj_list[self.selected]:
            self.adj_list[self.selected].remove(bt_id)
            self.lns[self.selected][bt_id].set(QPoint(-100, 100), QPoint(-100, -100))
        else:
            self.adj_list[self.selected].append(bt_id)
        self.unselect(-1)

    def add_vertex(self):
        for i, l in enumerate(self.adj_list):
            for j in l:
                self.lns[i][j].set(QPoint(-100, -100), QPoint(-100, -1000))
        self.adj_list.append([])

        self.n += 1
        self.lns = [[Line(self.bg, self.size) for _ in range(self.n)] for _ in range(self.n)]
        self.bt.append(MovingButton(self, 10, 'black'))
        self.bt[-1].button.connect(self.add_edje, self.n-1)
        self.bt[-1].button.connect(self.unselect, self.n-1)
        self.bt[-1].set_pos(random.randint(0, self.size.x()), random.randint(0, self.size.y()))


class Window(QMainWindow):
    def __init__(self, pos, size):
        super().__init__()
        self.bg = QWidget(self)
        self.bg.setGeometry(0, 0, size.x(), size.y())
        self.g = Graph(self, 0, size)
        self.setWindowTitle('Тестовая рисовалка')
        self.setGeometry(pos.x(), pos.y(), size.x(), size.y())

        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        filemenu = QMenu("&Файл", self)
        nodemenu = QMenu("&Вершина", self)
        menubar.addMenu(filemenu)
        menubar.addMenu(nodemenu)

        filemenu.addAction("Открыть", self.clicked).setShortcut("Ctrl+O")
        filemenu.addAction("Сохранить", self.clicked).setShortcut("Ctrl+S")
        filemenu.addAction("Сохранить как", self.clicked).setShortcut("Ctrl+Shift+S")
        filemenu.addAction("Выйти", self.clicked).setShortcut("Alt+F4")
        nodemenu.addAction("Добавить", self.clicked).setShortcut("Ctrl+N")
        self.show()

    @QtCore.pyqtSlot()
    def clicked(self):
        match self.sender().text():
            case "Открыть":
                print("Открыть")
                files = QFileDialog.getOpenFileName(self)[0]
                print(files)
            case "Сохранить":
                print("Сохранить")
                print(self.g.adj_list)
            case "Сохранить как":
                print("Сохранить как")
            case "Выйти":
                print("Выйти")
                sys.exit()
            case "Добавить":
                self.close()
                self.g.add_vertex()
                self.show()
            case _:
                print("defautl")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window(QPoint(200, 200), QPoint(1000, 500))
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-
import sys
import copy
import numpy
from PyQt5.Qt import QGraphicsView, QGraphicsItem, QApplication, Qt
from PyQt5.Qt import QGraphicsScene, QPainter, QStyleOptionGraphicsItem
from PyQt5.Qt import QGraphicsSceneMouseEvent
from PyQt5.Qt import QKeyEvent, QMouseEvent, QTimer
from PyQt5.Qt import QImage, QScreen
from PyQt5.Qt import QPoint, QRectF, QPen, QRect


class Body(QGraphicsItem):
    def __init__(self,parent, width, height):
        super().__init__(parent=parent)
        self.width = width
        self.height = height
        # self.setOpacity(0.0)
        self.head_img = QImage("resource/a_oryzae.png")

    def paint(self, paint: QPainter, style: QStyleOptionGraphicsItem, widget=None):
        qpen = QPen()
        qpen.setColor(Qt.white)
        # paint.setBackground()
        paint.setPen(qpen)
        aspect = self.head_img.width() / self.head_img.height()
        ratio = self.height * 0.2
        target = QRectF(0, 0, aspect*ratio, ratio)
        source = QRectF(0, 0, self.head_img.width(), self.head_img.height())

        paint.drawImage(target, self.head_img, source)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)


class Agent(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        fp = open("css/client.css", "r")
        self.setStyleSheet(fp.read())
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)

        item = Body(self.parent(), self.width(), self.height())

        scene = QGraphicsScene()
        scene.addItem(item)

        self.setScene(scene)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.tmp_pos = QPoint(0, 0)

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Q:
            self.close()

    def mousePressEvent(self, e: QMouseEvent):
        self.tmp_pos = e.pos()

    def mouseMoveEvent(self, e: QMouseEvent):
        # self.diff_pos = e.pos() - self.diff_pos
        # print(diff+self.pos())
        mouse_pos = self.pos() + e.pos()
        self.move(mouse_pos-self.tmp_pos)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    agent = list()
    n = 50
    random_x = numpy.random.rand(n)
    random_y = numpy.random.rand(n)

    screen = app.primaryScreen() # type:QScreen
    screen_height = screen.geometry().height()
    screen_width = screen.geometry().width()

    for i in range(n):
        j = Agent()
        j.move(QPoint(random_x[i]*screen_width, random_y[i]*screen_height))
        j.show()
        agent.append(j)

    sys.exit(app.exec())

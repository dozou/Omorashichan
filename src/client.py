# -*- coding: utf-8 -*-
import sys
import copy
from PyQt5.Qt import QGraphicsView, QGraphicsItem, QApplication, Qt
from PyQt5.Qt import QGraphicsScene, QPainter, QStyleOptionGraphicsItem
from PyQt5.Qt import QGraphicsSceneMouseEvent
from PyQt5.Qt import QKeyEvent, QMouseEvent
from PyQt5.Qt import QImage
from PyQt5.Qt import QPoint, QRectF, QPen


class Agent(QGraphicsItem):
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
        ratio = self.height
        target = QRectF(0, 0, aspect*ratio, ratio)
        source = QRectF(0, 0, self.head_img.width(), self.head_img.height())

        paint.drawImage(target, self.head_img, source)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent):
        print("qa")

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)


class Window(QGraphicsView):
    def __init__(self):
        super().__init__()
        fp = open("css/client.css", "r")
        self.setStyleSheet(fp.read())
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setAttribute(Qt.WA_DeleteOnClose)

        scene = QGraphicsScene()
        item = Agent(self.parent(), self.width(), self.height())
        scene.addItem(item)
        scene.setSceneRect(0, 0, self.width(), self.height())
        self.setScene(scene)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.tmp_pos = QPoint(0,0)

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Q:
            self.close()

    def mousePressEvent(self, e: QMouseEvent):
        print(e.button())
        self.tmp_pos = e.pos()

    def mouseMoveEvent(self, e: QMouseEvent):
        # self.diff_pos = e.pos() - self.diff_pos
        # print(diff+self.pos())
        mouse_pos = self.pos() + e.pos()
        self.move(mouse_pos-self.tmp_pos)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

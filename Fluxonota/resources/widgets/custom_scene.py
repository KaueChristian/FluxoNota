from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt

def CustomGraphicsScene():
    """
    Creates a custom graphics scene with a specific background color and grid lines.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 20
        self.grid_pen = QPen(QColor(220, 220, 220), 0.5, Qt.PenStyle.DotLine)

    def drawBackground(self, painter, rect):
        """
        Draws the background of the scene with a grid pattern.
        """
        super().drawBackground(painter, rect)

        left = int(rect.left()) - int(rect.left()) % self.grid_size
        top = int(rect.top()) - int(rect.top()) % self.grid_size
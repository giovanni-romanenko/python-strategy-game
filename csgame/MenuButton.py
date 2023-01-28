import pyglet


class MenuButton:
    def __init__(self, x, y, dx, dy, labelText, batch=None,
                 groupNum=2, anchor_x='center', anchor_y='center'):
        self._x = x
        self._y = y
        self._dx = dx
        self._dy = dy
        self._size = len(labelText)
        self._label = pyglet.text.Label(labelText,
                                        font_name='Times New Roman',
                                        font_size=2 * self._dy // 3,
                                        x=self._x + self._dx // 2, y=self._y + self._dy // 2,
                                        anchor_x=anchor_x, anchor_y=anchor_y,
                                        group=pyglet.graphics.OrderedGroup(groupNum), batch=batch)

    def setButton(self, x, y, dx, dy):
        self._x = x
        self._y = y
        self._dx = dx
        self._dy = dy
        self._label.font_size = min(
            2 * self._dy // 3,
            (3 * self._dx) // self._size)
        self._label.x = self._x + self._dx // 2
        self._label.y = self._y + self._dy // 2

    def changeText(self, text):
        self._size = len(text)
        self._label.text = text

    def checkCursorOnButton(self, x, y):
        if (x >= self._label.x - self._label.content_width // 2 and x < self._label.x + self._label.content_width // 2 and
                y >= self._label.y - self._label.content_height // 2 and y < self._label.y + self._label.content_height // 2):
            return True
        return False

    def draw(self):
        self._label.draw()

    def changeBatch(self, batch):
        self._label.batch = batch

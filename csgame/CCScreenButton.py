import pyglet


class CCScreenButton:
    def __init__(self, x, y, width, height, character,
                 border, borderColor, batch, groupNum):
        character.setIcon(
            x,
            y,
            width,
            height,
            batch,
            pyglet.graphics.OrderedGroup(groupNum))
        self._sprite = character.getSprite()
        self._x = self._sprite.x
        self._y = self._sprite.y
        self._width = self._sprite.width
        self._height = self._sprite.height
        self._rightBorderLine = pyglet.shapes.Line(self._x + self._width, self._y - border // 2,
                                                   self._x + self._width, self._y + self._height + border // 2,
                                                   width=border, color=borderColor, batch=batch,
                                                   group=pyglet.graphics.OrderedGroup(groupNum + 1))
        self._upperBorderLine = pyglet.shapes.Line(self._x + self._width + border // 2, self._y + self._height,
                                                   self._x - border // 2, self._y + self._height,
                                                   width=border, color=borderColor, batch=batch,
                                                   group=pyglet.graphics.OrderedGroup(groupNum + 1))
        self._leftBorderLine = pyglet.shapes.Line(self._x, self._y + self._height + border // 2,
                                                  self._x, self._y - border // 2,
                                                  width=border, color=borderColor, batch=batch,
                                                  group=pyglet.graphics.OrderedGroup(groupNum + 1))
        self._lowerBorderLine = pyglet.shapes.Line(self._x - border // 2, self._y,
                                                   self._x + self._width + border // 2, self._y,
                                                   width=border, color=borderColor, batch=batch,
                                                   group=pyglet.graphics.OrderedGroup(groupNum + 1))

    def checkMouseIsOver(self, x, y):
        if x >= self._x and x < self._x + \
                self._width and y >= self._y and y < self._y + self._height:
            return True
        return False

    def changeBorderColor(self, color):
        self._rightBorderLine.color = color
        self._upperBorderLine.color = color
        self._leftBorderLine.color = color
        self._lowerBorderLine.color = color

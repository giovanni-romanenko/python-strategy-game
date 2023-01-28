import pyglet


class LowerRibbon:
    def __init__(self, x, y, width, height, color, batch, groupNum):
        self._rectangle = pyglet.shapes.Rectangle(
            x, y, width, height, color=color, batch=batch,
            group=pyglet.graphics.OrderedGroup(groupNum)
        )
        self._upperLine = pyglet.shapes.Line(x, y + height, x + width, y + height, width=5, color=color, batch=batch,
                                             group=pyglet.graphics.OrderedGroup(groupNum + 1))

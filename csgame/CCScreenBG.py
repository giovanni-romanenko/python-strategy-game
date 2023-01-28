import pyglet


class CCScreenBG:
    def __init__(self, window, gameInfo, batch, color1=(
            255, 250, 205), color2=(173, 216, 230), lineColor=(255, 192, 203)):
        self._window = window
        self._gameInfo = gameInfo
        self._BGRectangles = list()
        startPointX = self._window.width // (2 *
                                             (self._gameInfo.playerCnt + 1))
        ribbonWidth = self._window.width // (self._gameInfo.playerCnt + 1)
        ribbonHeight = (9 * self._window.height) // 10
        i = 0
        while i < self._gameInfo.playerCnt:
            if i % 2 == 0:
                self._BGRectangles.append(pyglet.shapes.Rectangle(startPointX + i * ribbonWidth, 0, ribbonWidth, ribbonHeight,
                                                                  color=color1, batch=batch, group=pyglet.graphics.OrderedGroup(0)))
            else:
                self._BGRectangles.append(pyglet.shapes.Rectangle(startPointX + i * ribbonWidth, 0, ribbonWidth, ribbonHeight,
                                                                  color=color2, batch=batch, group=pyglet.graphics.OrderedGroup(0)))
            i += 1
        self._leftRectangle = pyglet.shapes.Rectangle(0, 0, ribbonWidth // 2, ribbonHeight, color=color2, batch=batch,
                                                      group=pyglet.graphics.OrderedGroup(0))
        if self._gameInfo.playerCnt % 2 == 0:
            self._rightRectangle = pyglet.shapes.Rectangle(startPointX + (self._gameInfo.playerCnt * ribbonWidth), 0,
                                                           ribbonWidth // 2, ribbonHeight, color=color1, batch=batch,
                                                           group=pyglet.graphics.OrderedGroup(0))
        else:
            self._rightRectangle = pyglet.shapes.Rectangle(startPointX + (self._gameInfo.playerCnt * ribbonWidth), 0,
                                                           ribbonWidth // 2, ribbonHeight, color=color2, batch=batch,
                                                           group=pyglet.graphics.OrderedGroup(0))
        self._lowerLine = pyglet.shapes.Line(0, 0, self._window.width, 0, width=5, color=lineColor,
                                             batch=batch, group=pyglet.graphics.OrderedGroup(1))
        self._upperLine = pyglet.shapes.Line(0, ribbonHeight, self._window.width, ribbonHeight, width=5, color=lineColor,
                                             batch=batch, group=pyglet.graphics.OrderedGroup(1))
        self._leftLine = pyglet.shapes.Line(0, 0, 0, ribbonHeight, width=5, color=lineColor,
                                            batch=batch, group=pyglet.graphics.OrderedGroup(1))
        self._rightLine = pyglet.shapes.Line(self._window.width, 0, self._window.width, ribbonHeight, width=5, color=lineColor,
                                             batch=batch, group=pyglet.graphics.OrderedGroup(1))
        self._inBetweenLines = list()
        i = 0
        while i <= self._gameInfo.playerCnt:
            self._inBetweenLines.append(pyglet.shapes.Line(startPointX + i * ribbonWidth, 0,
                                                           startPointX + i * ribbonWidth, self._window.height,
                                                           width=5, color=lineColor, batch=batch,
                                                           group=pyglet.graphics.OrderedGroup(1)))
            i += 1
        self._playerLabels = list()
        i = 0
        while i < self._gameInfo.playerCnt:
            curFontSize = (self._window.height) // 20
            self._playerLabels.append(pyglet.text.Label(self._gameInfo.players[i].getName(),
                                                        font_name='Times New Roman', font_size=curFontSize,
                                                        color=(*self._gameInfo.players[i].getColor(), 255),
                                                        x=(i + 1) * ribbonWidth, y=(19 * self._window.height) // 20,
                                                        width=ribbonWidth, height=self._window.height // 10,
                                                        anchor_x='center', anchor_y='center', batch=batch,
                                                        group=pyglet.graphics.OrderedGroup(1)))
            i += 1

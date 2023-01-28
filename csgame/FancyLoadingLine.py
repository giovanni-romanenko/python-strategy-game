import pyglet


class FancyLoadingLine:
    def __init__(self, rectInfo, windowWidth, windowHeight, sec, borderColor=(192, 192, 192),
                 insideColor=(0, 0, 0), loadStartColor=(204, 51, 255), loadEndColor=(0, 255, 204), border=5):
        self._llBatch = pyglet.graphics.Batch()
        self._rectInfo = rectInfo
        self._windowWidth = windowWidth
        self._sec = sec
        self._mainRect = pyglet.shapes.BorderedRectangle(rectInfo[0] * windowWidth // rectInfo[1],
                                                         rectInfo[2] *
                                                         windowHeight // rectInfo[3],
                                                         rectInfo[4] *
                                                         windowWidth // rectInfo[5],
                                                         rectInfo[6] *
                                                         windowHeight // rectInfo[7],
                                                         color=insideColor, border_color=borderColor,
                                                         group=pyglet.graphics.OrderedGroup(
                                                             0),
                                                         batch=self._llBatch, border=border)
        self._loadRect = pyglet.shapes.Rectangle(rectInfo[0] * windowWidth // rectInfo[1] + border,
                                                 rectInfo[2] *
                                                 windowHeight // rectInfo[3] +
                                                 border,
                                                 0,
                                                 rectInfo[6] *
                                                 windowHeight // rectInfo[7] -
                                                 2 * border,
                                                 color=loadStartColor, group=pyglet.graphics.OrderedGroup(
                                                     2),
                                                 batch=self._llBatch)
        self._curTimeval = 0.0
        self._border = border
        self._finished = self._curTimeval == self._sec
        self._stR, self._stG, self._stB = loadStartColor
        self._endR, self._endG, self._endB = loadEndColor

    def draw(self):
        self._llBatch.draw()

    def updateOnTimeval(self, timeval):
        self._curTimeval += timeval
        if self._curTimeval > self._sec:
            self._curTimeval = self._sec
        ratio = (self._curTimeval / self._sec)
        self._loadRect.width = ratio * \
            (self._rectInfo[4] * self._windowWidth //
             self._rectInfo[5] - 2 * self._border)
        self._loadRect.color = ((1 - ratio) * self._stR + ratio * self._endR,
                                (1 - ratio) * self._stG + ratio * self._endG,
                                (1 - ratio) * self._stB + ratio * self._endB)
        self._finished = self._curTimeval == self._sec

    def updateOnResize(self, windowWidth, windowHeight):
        self._mainRect.x = self._rectInfo[0] * windowWidth // self._rectInfo[1]
        self._mainRect.y = self._rectInfo[2] * \
            windowHeight // self._rectInfo[3]
        self._mainRect.width = self._rectInfo[4] * \
            windowWidth // self._rectInfo[5]
        self._mainRect.height = self._rectInfo[6] * \
            windowHeight // self._rectInfo[7]
        self._loadRect.x = self._rectInfo[0] * \
            windowWidth // self._rectInfo[1] + self._border
        self._loadRect.y = self._rectInfo[2] * \
            windowHeight // self._rectInfo[3] + self._border
        self._loadRect.width = (self._curTimeval / self._sec) * (
            self._rectInfo[4] * windowWidth // self._rectInfo[5] - 2 * self._border)
        self._loadRect.height = self._rectInfo[6] * \
            windowHeight // self._rectInfo[7] - 2 * self._border
        self._windowWidth = windowWidth

    def finished(self):
        return self._finished

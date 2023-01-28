import pyglet
import words


class GSUpperRibbon:
    def __init__(self, gameInfo, x, y, width, height, batch,
                 groupNum, border, borderColor, time):
        self._BGColor = pyglet.shapes.Rectangle(
            x + (2 * width) // 5, y, (3 * width) // 5, height + border // 2, color=(225, 225, 225), batch=batch,
            group=pyglet.graphics.OrderedGroup(groupNum)
        )
        scoreText = str(
            gameInfo.currentResults[0]) + ":" + str(gameInfo.currentResults[1])
        scoreFontSize = 3 * height / 5
        self._scoreLabel = pyglet.text.Label(
            scoreText, font_name='Times New Roman', font_size=scoreFontSize,
            color=(0, 0, 0, 255),
            x=x + width // 2, y=y + height // 2,
            width=width // 5, height=height,
            anchor_x='center', anchor_y='center',
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._verticalLines = [
            pyglet.shapes.Line(x + (2 * width) // 5, y, x + (2 * width) // 5, y + height + (border // 4), width=border, color=borderColor,
                               batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 2)),
            pyglet.shapes.Line(x + (3 * width) // 5, y, x + (3 * width) // 5, y + height + (border // 4), width=border, color=borderColor,
                               batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 2)),
            pyglet.shapes.Line(x + (9 * width) // 10, y, x + (9 * width) // 10, y + height + (border // 4), width=border, color=borderColor,
                               batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 2))
        ]
        self._horizontalLine = pyglet.shapes.Line(
            x, y, x + width, y, width=border, color=borderColor, batch=batch,
            group=pyglet.graphics.OrderedGroup(groupNum + 2)
        )
        self._maxTime = time
        self._curTime = 0
        timeText = str(self._curTime)
        if len(timeText) == 1:
            timeText = "0" + timeText
        timeText = words.word.time() + ": " + timeText
        timeFontSize = 3 * height / 5
        self._timeLabel = pyglet.text.Label(
            timeText, font_name='Times New Roman', font_size=timeFontSize,
            color=(0, 0, 0, 255),
            x=x + (3 * width) // 4, y=y + height // 2,
            width=(3 * width) // 10, height=height,
            anchor_x='center', anchor_y='center',
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        changeRendererFontSize = 3 * height / 5
        self._changeRendererLabel = pyglet.text.Label(
            "R", font_name='Times New Roman', font_size=changeRendererFontSize,
            color=(0, 0, 0, 255),
            x=x + (19 * width) // 20, y=y + height // 2,
            width=width // 10, height=height,
            anchor_x='center', anchor_y='center',
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._curCellType = None
        self._defaultDescriptionBGRectColor = (225, 225, 225)
        self._cellDescriptionBGRect = pyglet.shapes.Rectangle(
            x, y, (2 * width) // 5, height + border // 2, color=self._defaultDescriptionBGRectColor, batch=batch,
            group=pyglet.graphics.OrderedGroup(groupNum)
        )
        self._cellDescriptionLines = [
            pyglet.shapes.Line(x + (2 * width) // 15, y, x + (2 * width) // 15, y + height + (border // 4), width=border, color=borderColor,
                               batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 2)),
            pyglet.shapes.Line(x, y + height // 2, x + (2 * width) // 15, y + height // 2, width=border, color=borderColor,
                               batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 2)),
        ]
        self._cellDescriptionNameDocument = pyglet.text.document.UnformattedDocument(
            "")
        self._cellDescriptionNameDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=height // 5, align="center", color=(0, 0, 0, 255))
        )
        self._cellDescriptionNameLayout = pyglet.text.layout.TextLayout(
            self._cellDescriptionNameDocument, width=(2 * width) // 15, height=height // 2, multiline=True, wrap_lines=False,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._cellDescriptionNameLayout.x = x
        self._cellDescriptionNameLayout.y = y + height // 2
        self._cellDescriptionNameLayout.anchor_x = "left"
        self._cellDescriptionNameLayout.anchor_y = "bottom"
        self._cellDescriptionNameLayout.content_valign = "center"
        self._cellDescriptionAttrDocument = pyglet.text.document.UnformattedDocument(
            "")
        self._cellDescriptionAttrDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=height // 5, align="center", color=(0, 0, 0, 255))
        )
        self._cellDescriptionAttrLayout = pyglet.text.layout.TextLayout(
            self._cellDescriptionAttrDocument, width=(2 * width) // 15, height=height // 2, multiline=True, wrap_lines=False,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._cellDescriptionAttrLayout.x = x
        self._cellDescriptionAttrLayout.y = y
        self._cellDescriptionAttrLayout.anchor_x = "left"
        self._cellDescriptionAttrLayout.anchor_y = "bottom"
        self._cellDescriptionAttrLayout.content_valign = "center"
        self._cellDescriptionDescDocument = pyglet.text.document.UnformattedDocument(
            "")
        self._cellDescriptionDescDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=height // 5, color=(0, 0, 0, 255))
        )
        self._cellDescriptionDescLayout = pyglet.text.layout.TextLayout(
            self._cellDescriptionDescDocument, width=((4 * width) // 15) - (4 * border), height=height, multiline=True, wrap_lines=True,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._cellDescriptionDescLayout.x = x + \
            ((2 * width) // 15) + (2 * border)
        self._cellDescriptionDescLayout.y = y
        self._cellDescriptionDescLayout.anchor_x = "left"
        self._cellDescriptionDescLayout.anchor_y = "bottom"
        self._cellDescriptionDescLayout.content_valign = "center"

    def setMaxTime(self):
        self._curTime = self._maxTime
        self._changeTimeLabel()

    def addSeconds(self, seconds):
        self._curTime = min(90, self._curTime + seconds)
        self._changeTimeLabel()

    def countDown(self):
        self._curTime -= 1
        self._changeTimeLabel()

    def _changeTimeLabel(self):
        timeText = str(self._curTime)
        if len(timeText) == 1:
            timeText = "0" + timeText
        timeText = words.word.time() + ": " + timeText
        self._timeLabel.text = timeText

    def getCurTime(self):
        return self._curTime

    def changeCellTypeInfo(self, cellType):
        if self._curCellType is cellType:
            return False
        self._curCellType = cellType
        if self._curCellType is None:
            self._cellDescriptionNameLayout.document.text = ""
            self._cellDescriptionAttrLayout.document.text = ""
            self._cellDescriptionDescLayout.document.text = ""
            return True
        curCTName = self._curCellType.getName()
        self._cellDescriptionNameLayout.document.text = words.word.cellTypeName(
            curCTName)
        if self._curCellType.isWatery():
            self._cellDescriptionAttrLayout.document.text = words.word.watery()
        else:
            self._cellDescriptionAttrLayout.document.text = words.word.nonWatery()
        self._cellDescriptionDescLayout.document.text = words.word.cellTypeDescription(
            curCTName)
        return True

    def checkMouseOnChangeRendererButton(self, x, y):
        if (x >= self._changeRendererLabel.x - self._changeRendererLabel.content_width // 2
            and x < self._changeRendererLabel.x + self._changeRendererLabel.content_width // 2
            and y >= self._changeRendererLabel.y - self._changeRendererLabel.content_height // 2
                and y < self._changeRendererLabel.y + self._changeRendererLabel.content_height // 2):
            return True
        return False

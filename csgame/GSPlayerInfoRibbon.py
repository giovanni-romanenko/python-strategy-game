import pyglet
import words


class GSPlayerInfoRibbon:
    def __init__(self, gamePosition, player, character, x, y, width, height, batch, border, borderColor, borderPassiveColor,
                 borderActiveColor, groupNum, side, mainBorder):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._border = border
        self._batch = batch
        self._groupNum = groupNum
        self._borderPassiveColor = borderPassiveColor
        self._borderActiveColor = borderActiveColor
        self._BGRectanglePlayerName = pyglet.shapes.Rectangle(
            x - (border // 4), y + ((9 * height) // 10), width +
            (border // 2), (height // 10) + (border // 4),
            color=(70, 70, 70), batch=batch,
            group=pyglet.graphics.OrderedGroup(groupNum)
        )
        playerNameFontSize = min(
            (5 * width) / (4 * len(player.getName())), height / 23)
        self._playerNameDocument = pyglet.text.document.UnformattedDocument(
            player.getName())
        self._playerNameDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=playerNameFontSize,
                                            align="center", color=(*player.getColor(), 255))
        )
        self._playerNameLayout = pyglet.text.layout.TextLayout(
            self._playerNameDocument, width=width - (2 * border), height=(height // 10), multiline=True, wrap_lines=False,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._playerNameLayout.x = x + border
        self._playerNameLayout.y = y + ((9 * height) // 10)
        self._playerNameLayout.anchor_x = "left"
        self._playerNameLayout.anchor_y = "bottom"
        self._playerNameLayout.content_valign = "center"
        character.setIcon(x - (border // 4), y + ((163 * height) // 270) - (border // 4), width + (border // 2), ((8 * height) / 27) + (border // 2),
                          batch, pyglet.graphics.OrderedGroup(groupNum))
        self._characterInfoBGRect = pyglet.shapes.Rectangle(
            x - (border // 4), y - (border // 4), width +
            (border // 2), (163 * height // 270) + (border // 2),
            color=(15, 15, 15), batch=batch,
            group=pyglet.graphics.OrderedGroup(groupNum)
        )
        self._character = character
        self._charNameDocument = pyglet.text.document.UnformattedDocument(
            words.word.characterName(self._character.getName()))
        self._charNameDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=height / 30, align="center", color=(225, 225, 0, 255))
        )
        self._charNameLayout = pyglet.text.layout.TextLayout(
            self._charNameDocument, width=width - (2 * border), height=(2 * height) // 27, multiline=True, wrap_lines=False,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._charNameLayout.x = x + border
        self._charNameLayout.y = y + (143 * height) // 270
        self._charNameLayout.anchor_x = "left"
        self._charNameLayout.anchor_y = "bottom"
        self._charNameLayout.content_valign = "center"
        if self._character.isHoly():
            self._charAttrDocument = pyglet.text.document.UnformattedDocument(
                words.word.holy())
        else:
            self._charAttrDocument = pyglet.text.document.UnformattedDocument(
                words.word.unholy())
        self._charAttrDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=height / 48, align="center", color=(225, 225, 0, 255))
        )
        self._charAttrLayout = pyglet.text.layout.TextLayout(
            self._charAttrDocument, width=(width // 3) - border, height=(2 * height) // 45, multiline=True, wrap_lines=False,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._charAttrLayout.x = x + ((2 * width) // 3) + border // 2
        self._charAttrLayout.y = y + (131 * height) // 270
        self._charAttrLayout.anchor_x = "left"
        self._charAttrLayout.anchor_y = "bottom"
        self._charAttrLayout.content_valign = "center"
        self._charDescDocumet = pyglet.text.document.UnformattedDocument(
            words.word.characterRulesDescription(self._character.getName()))
        self._charDescDocumet.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=height / 50, align="left", color=(230, 230, 230, 255))
        )
        self._charDescLayout = pyglet.text.layout.TextLayout(
            self._charDescDocumet, width=width - (2 * border), height=(10 * height) // 27, multiline=True, wrap_lines=False,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._charDescLayout.x = x + border
        self._charDescLayout.y = y + height // 10
        self._charDescLayout.anchor_x = "left"
        self._charDescLayout.anchor_y = "bottom"
        self._charDescLayout.content_valign = "top"
        self._charGameDataDocument = pyglet.text.document.UnformattedDocument(
            "")
        self._charGameDataDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=height / 40, align="left", color=(230, 230, 230, 255))
        )
        self._charGameDataLayout = pyglet.text.layout.TextLayout(
            self._charGameDataDocument, width=width - (4 * border), height=((3 * height) // 20) - (2 * border), multiline=True, wrap_lines=False,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._charGameDataLayout.x = x + (2 * border)
        self._charGameDataLayout.y = y
        self._charGameDataLayout.anchor_x = "left"
        self._charGameDataLayout.anchor_y = "bottom"
        self._charGameDataLayout.content_valign = "top"
        self._charGameDataLayout.document.text = self._character.getCharGameDataText(
            gamePosition, None)
        self._insideLines = [
            pyglet.shapes.Line(x - (border // 4), y + (9 * height) // 10, x + width, y + (9 * height) // 10,
                               width=border, color=borderColor, batch=batch,
                               group=pyglet.graphics.OrderedGroup(groupNum + 2)),
            pyglet.shapes.Line(x - (border // 4), y + (163 * height) // 270, x + width, y + (163 * height) // 270,
                               width=border, color=borderColor, batch=batch,
                               group=pyglet.graphics.OrderedGroup(groupNum + 2)),
            pyglet.shapes.Line(x - (border // 4), y + (3 * height) // 20, x + width, y + (3 * height) // 20,
                               width=border, color=borderColor, batch=batch,
                               group=pyglet.graphics.OrderedGroup(groupNum + 2)),
            pyglet.shapes.Line(x + ((2 * width) // 3) - (border // 4), y + (131 * height // 270), x + width, y + (131 * height // 270),
                               width=border // 2, color=borderColor, batch=batch,
                               group=pyglet.graphics.OrderedGroup(groupNum + 2)),
            pyglet.shapes.Line(x + ((2 * width) // 3), y + (131 * height // 270) - (border // 4), x + ((2 * width) // 3), y + (143 * height) // 270,
                               width=border // 2, color=borderColor, batch=batch,
                               group=pyglet.graphics.OrderedGroup(groupNum + 2)),
            pyglet.shapes.Line(x - (border // 4), y + (143 * height) // 270, x + width, y + (143 * height) // 270,
                               width=border, color=borderColor, batch=batch,
                               group=pyglet.graphics.OrderedGroup(groupNum + 2))
        ]
        vertLineX = x + width
        if side == 'left':
            vertLineX = x
        self._mainVerticalLine = pyglet.shapes.Line(
            vertLineX, y - (border // 4), vertLineX, y +
            height + (border // 2),
            width=mainBorder, color=borderPassiveColor, batch=batch,
            group=pyglet.graphics.OrderedGroup(groupNum + 3)
        )

    def onGameChange(self, character, gamePosition, playerNum):
        if self._character is not character:
            self._character = character
            self._charNameLayout.document.text = words.word.characterName(
                self._character.getName())
            if self._character.isHoly():
                self._charAttrLayout.document.text = words.word.holy()
            else:
                self._charAttrLayout.document.text = words.word.unholy()
            self._charDescLayout.document.text = words.word.characterRulesDescription(
                self._character.getName())
            self._character.setIcon(
                self._x - (self._border // 4), self._y +
                ((163 * self._height) // 270) - (self._border // 4),
                self._width + (self._border // 2), ((8 *
                                                     self._height) / 27) + (self._border // 2),
                self._batch, pyglet.graphics.OrderedGroup(self._groupNum)
            )
        self._charGameDataLayout.document.text = self._character.getCharGameDataText(
            gamePosition, playerNum)

    def turnOnActiveColor(self):
        if self._mainVerticalLine.color != self._borderActiveColor:
            self._mainVerticalLine.color = self._borderActiveColor

    def turnOnPassiveColor(self):
        if self._mainVerticalLine.color != self._borderPassiveColor:
            self._mainVerticalLine.color = self._borderPassiveColor

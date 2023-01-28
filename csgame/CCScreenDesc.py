import pyglet
import words


class CCScreenDesc:
    def __init__(self, x, y, width, height, character, batch,
                 groupNum, bgColor, border, borderColor, textColor):
        self._descBGRect = pyglet.shapes.BorderedRectangle(
            x, y, width, height, border=border, color=bgColor, border_color=borderColor,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum)
        )
        self._descBGRect.opacity = 0
        self._character = character
        self._charDescNameText = words.word.characterName(
            self._character.getName())
        self._charDescNameDocument = pyglet.text.document.UnformattedDocument(
            self._charDescNameText)
        self._charDescNameDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=height / 14, align="center", color=textColor)
        )
        self._charDescNameLayout = pyglet.text.layout.TextLayout(
            self._charDescNameDocument, width=width, height=height // 8, multiline=True, wrap_lines=False,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._charDescNameLayout.x = x
        self._charDescNameLayout.y = y + (7 * height) // 8
        self._charDescNameLayout.anchor_x = "left"
        self._charDescNameLayout.anchor_y = "bottom"
        self._charDescNameLayout.content_valign = "bottom"
        self._charDescNameLayout.document.text = ""
        if self._character.isHoly():
            self._charDescAttrText = words.word.holy()
        else:
            self._charDescAttrText = words.word.unholy()
        self._charDescAttrDocument = pyglet.text.document.UnformattedDocument(
            self._charDescAttrText)
        self._charDescAttrDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=height / 20, align="right", color=textColor)
        )
        self._charDescAttrLayout = pyglet.text.layout.TextLayout(
            self._charDescAttrDocument, width=width - (4 * border), height=height // 10, multiline=True, wrap_lines=False,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._charDescAttrLayout.x = x + (2 * border)
        self._charDescAttrLayout.y = y + (31 * height) // 40
        self._charDescAttrLayout.anchor_x = "left"
        self._charDescAttrLayout.anchor_y = "bottom"
        self._charDescAttrLayout.content_valign = "center"
        self._charDescAttrLayout.document.text = ""
        self._charDescRulesText = words.word.characterRulesDescription(
            self._character.getName())
        self._charDescRulesDocument = pyglet.text.document.UnformattedDocument(
            self._charDescRulesText)
        self._charDescRulesDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=height / 20, align="left", color=textColor)
        )
        self._charDescRulesLayout = pyglet.text.layout.TextLayout(
            self._charDescRulesDocument, width=width - (4 * border), height=(31 * height) // 40, multiline=True, wrap_lines=False,
            batch=batch, group=pyglet.graphics.OrderedGroup(groupNum + 1)
        )
        self._charDescRulesLayout.x = x + (2 * border)
        self._charDescRulesLayout.y = y
        self._charDescRulesLayout.anchor_x = "left"
        self._charDescRulesLayout.anchor_y = "bottom"
        self._charDescRulesLayout.content_valign = "top"
        self._charDescRulesLayout.document.text = ""

    def makeVisible(self):
        self._descBGRect.opacity = 255
        self._charDescNameLayout.document.text = self._charDescNameText
        self._charDescAttrLayout.document.text = self._charDescAttrText
        self._charDescRulesLayout.document.text = self._charDescRulesText

    def makeInvisible(self):
        self._descBGRect.opacity = 0
        self._charDescNameLayout.document.text = ""
        self._charDescAttrLayout.document.text = ""
        self._charDescRulesLayout.document.text = ""

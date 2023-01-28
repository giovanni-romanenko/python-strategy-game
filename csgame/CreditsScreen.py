import pyglet
import words
from .MenuButton import MenuButton


class CreditsScreen:
    def __init__(self, window, parent):
        self._window = window
        self._parent = parent
        self._screenBatch = pyglet.graphics.Batch()
        self._language = words.word.currentLanguage()
        self._listOfButtonsInfo = [[4, 5, 3, 4, 1, 7, 1, 5, 'X']]
        self._listOfButtons = list()
        for buttonInfo in self._listOfButtonsInfo:
            self._listOfButtons.append(
                MenuButton(buttonInfo[0] * self._window.width // buttonInfo[1], buttonInfo[2] * self._window.height // buttonInfo[3],
                           buttonInfo[4] * self._window.width // buttonInfo[5], buttonInfo[6] *
                           self._window.height // buttonInfo[7],
                           buttonInfo[8], batch=self._screenBatch))
        self._listOfReactions = [self._screenEnd]
        self._listOfText = [words.word.createdBy(), words.word.musicBy()]
        self._listOfLabelInfo = [[-1, 8, 7, 10, 2, 5, 1, 20, self._listOfText[0]],
                                 [-1, 8, 3, 5, 2, 5, 1, 20, self._listOfText[1]]]
        self._listOfLabels = list()
        for labelInfo in self._listOfLabelInfo:
            self._listOfLabels.append(
                MenuButton(labelInfo[0] * self._window.width // labelInfo[1], labelInfo[2] * self._window.height // labelInfo[3],
                           labelInfo[4] * self._window.width // labelInfo[5], labelInfo[6] *
                           self._window.height // labelInfo[7],
                           labelInfo[8], batch=self._screenBatch, anchor_x='left', anchor_y='baseline'))
        self._BGSprite = pyglet.sprite.Sprite(img=pyglet.resource.image('MenuBG.png'), group=pyglet.graphics.OrderedGroup(0),
                                              batch=self._screenBatch)

    def _changeDataDependentOnLanguage(self):
        self._language = words.word.currentLanguage()
        self._listOfText = [words.word.createdBy(), words.word.musicBy()]
        self._listOfLabelInfo = [[-1, 8, 7, 10, 2, 5, 1, 20, self._listOfText[0]],
                                 [-1, 8, 3, 5, 2, 5, 1, 20, self._listOfText[1]]]
        i = 0
        for label in self._listOfLabels:
            label.changeText(self._listOfLabelInfo[i][8])
            i += 1

    def screenInit(self):
        self._window.push_handlers(on_key_press=self._onKeyPress, on_mouse_press=self._onMousePress, on_draw=self._onDraw,
                                   on_resize=self._onResize)
        if self._language != words.word.currentLanguage():
            self._changeDataDependentOnLanguage()
        self._onResize(self._window.width, self._window.height)

    def _screenEnd(self):
        self._window.pop_handlers()
        self._parent.screenInit()

    def _onKeyPress(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self._screenEnd()
        return True

    def _onMousePress(self, x, y, button, modifiers):
        if self._listOfButtons[0].checkCursorOnButton(x, y):
            self._listOfReactions[0]()
        return True

    def _onDraw(self):
        self._window.clear()
        self._screenBatch.draw()
        return True

    def _onResize(self, width, height):
        i = 0
        for buttonInfo in self._listOfButtonsInfo:
            self._listOfButtons[i].setButton(buttonInfo[0] * self._window.width // buttonInfo[1],
                                             buttonInfo[2] *
                                             self._window.height // buttonInfo[3],
                                             buttonInfo[4] *
                                             self._window.width // buttonInfo[5],
                                             buttonInfo[6] * self._window.height // buttonInfo[7])
            i += 1
        i = 0
        for labelInfo in self._listOfLabelInfo:
            self._listOfLabels[i].setButton(labelInfo[0] * self._window.width // labelInfo[1],
                                            labelInfo[2] *
                                            self._window.height // labelInfo[3],
                                            labelInfo[4] *
                                            self._window.width // labelInfo[5],
                                            labelInfo[6] * self._window.height // labelInfo[7])
            i += 1
        self._BGSprite.scale_x = self._BGSprite.scale_x * \
            (self._window.width / self._BGSprite.width)
        self._BGSprite.scale_y = self._BGSprite.scale_y * \
            (self._window.height / self._BGSprite.height)

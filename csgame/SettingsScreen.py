import pyglet
import words
from .MenuButton import MenuButton


class SettingsScreen:
    def __init__(self, window, parent, player):
        self._window = window
        self._parent = parent
        self._screenBatch = pyglet.graphics.Batch()
        self._player = player
        self._language = words.word.currentLanguage()
        self._languageText = words.word.language() + ": " + words.word.currentLanguage()
        self._fullscreenText = words.word.fullscreen() + ": "
        if self._window.fullscreen:
            self._fullscreenText += words.word.on()
        else:
            self._fullscreenText += words.word.off()
        self._listOfButtonsInfo = [[4, 5, 3, 4, 1, 7, 1, 5, 'X'],
                                   [3, 8, 13, 24, 1, 4, 1, 10, self._languageText],
                                   [3, 8, 5, 12, 1, 4, 1, 10,
                                       self._fullscreenText],
                                   [3, 8, 7, 24, 1, 4, 1, 10,
                                       words.word.musicVolume()],
                                   [7, 16, 5, 24, 1, 32, 1, 10, '<'],
                                   [8, 16, 5, 24, 1, 32, 1, 10, '>']]
        self._listOfButtons = list()
        for buttonInfo in self._listOfButtonsInfo:
            self._listOfButtons.append(
                MenuButton(buttonInfo[0] * self._window.width // buttonInfo[1], buttonInfo[2] * self._window.height // buttonInfo[3],
                           buttonInfo[4] * self._window.width // buttonInfo[5], buttonInfo[6] *
                           self._window.height // buttonInfo[7],
                           buttonInfo[8], batch=self._screenBatch))
        self._listOfReactions = [self._screenEnd, self._languageReaction, self._fullscreenReaction, self._dummyReaction,
                                 self._turnDownMusicVolumeReaction, self._turnUpMusicVolumeReaction]
        self._BGSprite = pyglet.sprite.Sprite(img=pyglet.resource.image('MenuBG.png'), group=pyglet.graphics.OrderedGroup(0),
                                              batch=self._screenBatch)

    def _changeDataDependentOnLanguage(self):
        self._language = words.word.currentLanguage()
        self._languageText = words.word.language() + ": " + words.word.currentLanguage()
        self._fullscreenText = words.word.fullscreen() + ": "
        if self._window.fullscreen:
            self._fullscreenText += words.word.on()
        else:
            self._fullscreenText += words.word.off()
        self._listOfButtonsInfo = [[4, 5, 3, 4, 1, 7, 1, 5, 'X'],
                                   [3, 8, 13, 24, 1, 4, 1, 10, self._languageText],
                                   [3, 8, 5, 12, 1, 4, 1, 10,
                                       self._fullscreenText],
                                   [3, 8, 7, 24, 1, 4, 1, 10,
                                       words.word.musicVolume()],
                                   [7, 16, 5, 24, 1, 32, 1, 10, '<'],
                                   [8, 16, 5, 24, 1, 32, 1, 10, '>']]
        i = 0
        for button in self._listOfButtons:
            button.changeText(self._listOfButtonsInfo[i][8])
            i += 1
        self._onResize(self._window.width, self._window.height)

    def screenInit(self):
        self._window.push_handlers(on_key_press=self._onKeyPress, on_mouse_press=self._onMousePress, on_draw=self._onDraw,
                                   on_resize=self._onResize)
        if self._language != words.word.currentLanguage():
            self._changeDataDependentOnLanguage()
        self._onResize(self._window.width, self._window.height)

    def _screenEnd(self):
        self._window.pop_handlers()
        self._parent.screenInit()

    def _languageReaction(self):
        words.setNextLanguage()
        if self._language != words.word.currentLanguage():
            self._changeDataDependentOnLanguage()

    def _fullscreenReaction(self):
        self._window.set_fullscreen(
            True) if not self._window.fullscreen else self._window.set_fullscreen(False)
        if self._window.fullscreen:
            self._fullscreenText = words.word.fullscreen() + ": " + words.word.on()
        else:
            self._fullscreenText = words.word.fullscreen() + ": " + words.word.off()
        self._listOfButtons[2].changeText(self._fullscreenText)

    def _dummyReaction(self):
        pass

    def _turnDownMusicVolumeReaction(self):
        if self._player.volume != 0.0:
            if self._player.volume / 2 >= 0.003:
                self._player.volume = self._player.volume / 2
            else:
                self._player.volume = 0.0

    def _turnUpMusicVolumeReaction(self):
        if self._player.volume == 0.0:
            self._player.volume = 0.003
        elif self._player.volume * 2 <= 4.0:
            self._player.volume = self._player.volume * 2
        else:
            self._player.volume = 4.0

    def _onKeyPress(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self._screenEnd()
        return True

    def _onMousePress(self, x, y, button, modifiers):
        i = 0
        for button in self._listOfButtons:
            if button.checkCursorOnButton(x, y):
                self._listOfReactions[i]()
            i += 1
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
        self._BGSprite.scale_x = self._BGSprite.scale_x * \
            (self._window.width / self._BGSprite.width)
        self._BGSprite.scale_y = self._BGSprite.scale_y * \
            (self._window.height / self._BGSprite.height)

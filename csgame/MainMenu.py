import pyglet
import words
from .MenuButton import MenuButton
from .CreditsScreen import CreditsScreen
from .SettingsScreen import SettingsScreen
from .GameSetupScreen import GameSetupScreen


class MainMenu:
    def __init__(self, window):
        self._window = window
        self._screenBatch = pyglet.graphics.Batch()
        self._language = words.word.currentLanguage()
        self._mediaPlayer = pyglet.media.Player()
        self._mediaPlayer.queue(pyglet.resource.media('menu.mp3'))
        self._mediaPlayer.loop = True
        self._mediaPlayer.volume = 0.1
        self._gameSetupScreen = GameSetupScreen(
            self._window, self, self._mediaPlayer, self)
        self._settingsScreen = SettingsScreen(
            self._window, self, self._mediaPlayer)
        self._creditsScreen = CreditsScreen(self._window, self)
        self._listOfButtonsInfo = [[3, 8, 13, 24, 1, 4, 1, 10, words.word.newGame()],
                                   [3, 8, 5, 12, 1, 4, 1, 10,
                                       words.word.settings()],
                                   [3, 8, 7, 24, 1, 4, 1, 10,
                                       words.word.credits()],
                                   [3, 8, 1, 6, 1, 4, 1, 10, words.word.exit()]]
        self._listOfButtons = list()
        for buttonInfo in self._listOfButtonsInfo:
            self._listOfButtons.append(
                MenuButton(buttonInfo[0] * self._window.width // buttonInfo[1], buttonInfo[2] * self._window.height // buttonInfo[3],
                           buttonInfo[4] * self._window.width // buttonInfo[5], buttonInfo[6] *
                           self._window.height // buttonInfo[7],
                           buttonInfo[8], batch=self._screenBatch))
        self._listOfReactions = [
            self._newGameReaction,
            self._settingsReaction,
            self._creditsReaction,
            self._exitReaction]
        self._BGSprite = pyglet.sprite.Sprite(img=pyglet.resource.image('MenuBG.png'), group=pyglet.graphics.OrderedGroup(0),
                                              batch=self._screenBatch)

    def _changeDataDependentOnLanguage(self):
        self._language = words.word.currentLanguage()
        self._listOfButtonsInfo = [[3, 8, 13, 24, 1, 4, 1, 10, words.word.newGame()],
                                   [3, 8, 5, 12, 1, 4, 1, 10,
                                       words.word.settings()],
                                   [3, 8, 7, 24, 1, 4, 1, 10,
                                       words.word.credits()],
                                   [3, 8, 1, 6, 1, 4, 1, 10, words.word.exit()]]
        i = 0
        for button in self._listOfButtons:
            button.changeText(self._listOfButtonsInfo[i][8])
            i += 1

    def screenInit(self):
        self._window.push_handlers(on_key_press=self._onKeyPress, on_mouse_press=self._onMousePress, on_draw=self._onDraw,
                                   on_resize=self._onResize)
        self._mediaPlayer.play()
        if self._language != words.word.currentLanguage():
            self._changeDataDependentOnLanguage()
        self._onResize(self._window.width, self._window.height)

    def _screenEnd(self):
        self._window.pop_handlers()

    def _newGameReaction(self):
        self._screenEnd()
        self._gameSetupScreen.screenInit()

    def _settingsReaction(self):
        self._screenEnd()
        self._settingsScreen.screenInit()

    def _creditsReaction(self):
        self._screenEnd()
        self._creditsScreen.screenInit()

    def _exitReaction(self):
        self._window.close()

    def _onKeyPress(self, symbol, modifiers):
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

import time
import pyglet
from .GamePause import GamePause
from .FancyLoadingLine import FancyLoadingLine
from .CharChoiceScreen import CharChoiceScreen
from .chargenerators.CharGen import CharGen
from .chargenerators.CharGenRandList import CharGenRandList


class GInitScreen:
    def __init__(self, window, endWindow):
        self._window = window
        self._endWindow = endWindow

    def screenInit(self, gameInfo, volume):
        self._loadingLine = FancyLoadingLine(
            [1, 5, 9, 20, 3, 5, 1, 10], self._window.width, self._window.height, 2.5)
        self._pauseScreen = GamePause(self._window, self)
        self._gameInfo = gameInfo
        self._volume = volume
        self._charGen = CharGenRandList()
        self.screenContinue()

    def screenContinue(self):
        self._window.push_handlers(on_key_press=self._onKeyPress, on_mouse_press=self._onMousePress, on_draw=self._onDraw,
                                   on_resize=self._onResize)
        self._onResize(self._window.width, self._window.height)
        self._timeval = time.time()
        pyglet.clock.schedule_interval(self._onDrawScheduled, 1 / 60)

    def _screenEnd(self):
        self._charGen.generateCharactersToChooseFrom(
            self._gameInfo.charChoiceList, self._gameInfo.characters)
        self._gameMediaPlayer = pyglet.media.Player()
        self._gameMediaList = ['Kai_Engel_-_06_-_Remedy_for_Melancholy.mp3',
                               'Kai_Engel_-_09_-_Sunset.mp3',
                               'Kevin_MacLeod_-_Erik_Satie_Gymnopedie_No_1.mp3',
                               'Kevin_MacLeod_-_J_S_Bach_Prelude_in_C_-_BWV_846.mp3',
                               'Kevin_MacLeod_-_Schmetterling.mp3',
                               'Misha_Dioxin_-_05_-_Arrival.mp3']
        self._gameMediaPlayer.volume = self._volume
        self._charChoiceMediaPlayer = pyglet.media.Player()
        self._charCMList = ['Misha_Dioxin_-_05_-_Arrival.mp3']
        for source in self._charCMList:
            self._charChoiceMediaPlayer.queue(pyglet.resource.media(source))
        self._charChoiceMediaPlayer.loop = True
        self._charChoiceMediaPlayer.volume = self._volume
        self._nextScreen = CharChoiceScreen(self._window, self._endWindow, self._gameMediaPlayer, self._gameMediaList,
                                            self._charChoiceMediaPlayer, self._pauseScreen)
        self._window.pop_handlers()
        pyglet.clock.unschedule(self._onDrawScheduled)
        self._nextScreen.screenInit(self._gameInfo, self._charGen.getResult())

    def _onKeyPress(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self._window.pop_handlers()
            pyglet.clock.unschedule(self._onDrawScheduled)
            self._pauseScreen.pause()
        return True

    def _onMousePress(self, x, y, button, modifiers):
        return True

    def _onDrawScheduled(self, dt):
        self._onDraw()

    def _onDraw(self):
        newTimeval = time.time()
        curTimeDiff = newTimeval - self._timeval
        self._timeval = newTimeval
        self._loadingLine.updateOnTimeval(curTimeDiff)
        self._window.clear()
        self._loadingLine.draw()
        if self._loadingLine.finished():
            self._screenEnd()
        return True

    def _onResize(self, width, height):
        self._loadingLine.updateOnResize(width, height)

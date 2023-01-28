import pyglet
import words
import numpy as np
from .GameMediaPlayer import GameMediaPlayer
from .GameScreen import GameScreen
from .GamePosition import GamePosition
from .fgenerators.FieldGen import FieldGen
from .fgenerators.FieldGenRand import FieldGenRand
from .scgenerators.StartCellGen import StartCellGen
from .scgenerators.StartCellGenRand import StartCellGenRand


class TransitionalScreen:
    def __init__(self, window, endWindow, gameMediaPlayer,
                 gameMediaList, pauseScreen):
        self._window = window
        self._endWindow = endWindow
        self._gameMediaPlayer = gameMediaPlayer
        self._gameMediaList = gameMediaList
        self._gamePlayer = GameMediaPlayer(
            self._gameMediaPlayer, self._gameMediaList)
        self._pauseScreen = pauseScreen
        self._fieldGen = FieldGenRand()
        self._startCellGen = StartCellGenRand()

    def screenInit(self, gameInfo):
        self._gameInfo = gameInfo
        self._gamePlayer.checkPlayingSource()
        self._gamePlayer.play()
        self.screenContinue()

    def screenContinue(self):
        self._window.push_handlers(
            on_key_press=self._onKeyPress,
            on_mouse_press=self._onMousePress,
            on_draw=self._onDraw)
        self._pauseScreen.setParent(self)
        self._gameInfo.restoreChangableData()
        if self._gameInfo.currentGameNum == self._gameInfo.gameCnt:
            self._gameEndShowResults()
            pyglet.clock.schedule_once(self._screenEndScheduled, 5.0)
            return None
        self._startTheNextGame()

    def _startTheNextGame(self):
        self._gamePosition = GamePosition(
            self._gameInfo, self._fieldGen, self._startCellGen)
        self._gameScreen = GameScreen(
            self._window,
            self,
            self._gamePlayer,
            self._pauseScreen,
            self._gameInfo,
            self._gamePosition)
        self._gameInfo.rememberChangableData()
        self._window.pop_handlers()
        self._gameScreen.screenInit()

    def _gameEndShowResults(self):
        if self._gamePlayer.isPlaying():
            self._gamePlayer.pause()
        self._window.pop_handlers()
        self._gameEndMessageDocument = pyglet.text.document.UnformattedDocument(
            "")
        self._gameEndMessageDocument.set_style(
            start=0, end=0, attributes=dict(font_name="Times New Roman", font_size=self._window.height / 10,
                                            align="center", color=(225, 225, 225, 255))
        )
        self._gameEndMessageLayout = pyglet.text.layout.TextLayout(
            self._gameEndMessageDocument, width=self._window.width, height=self._window.height, multiline=True, wrap_lines=True
        )
        self._gameEndMessageLayout.x = 0
        self._gameEndMessageLayout.y = 0
        self._gameEndMessageLayout.anchor_x = "left"
        self._gameEndMessageLayout.anchor_y = "bottom"
        self._gameEndMessageLayout.content_valign = "center"
        maxPnts = np.amax(self._gameInfo.currentResults)
        if self._gameInfo.playerCnt == 2 and self._gameInfo.currentResults[
                0] == self._gameInfo.currentResults[1]:
            self._gameEndMessageLayout.document.text = words.word.tieMessage()
        elif self._gameInfo.currentResults[self._gameInfo.playerOnScreen] == maxPnts:
            self._gameEndMessageLayout.document.text = words.word.victoryMessage()
        else:
            self._gameEndMessageLayout.document.text = words.word.lossMessage()
        self._window.push_handlers(
            on_key_press=self._onKeyPressGameEnd, on_mouse_press=self._onMousePressGameEnd, on_draw=self._onDrawGameEnd
        )

    def _screenEndScheduled(self, dt):
        self._screenEnd()

    def _screenEnd(self):
        if self._gamePlayer.isPlaying():
            self._gamePlayer.pause()
        self._window.pop_handlers()
        self._endWindow.screenInit()

    def _onKeyPress(self, symbol, modifiers):
        return True

    def _onMousePress(self, x, y, button, modifiers):
        return True

    def _onDraw(self):
        return True

    def _onKeyPressGameEnd(self, symbol, modifiers):
        return True

    def _onMousePressGameEnd(self, x, y, button, modifiers):
        return True

    def _onDrawGameEnd(self):
        self._window.clear()
        self._gameEndMessageLayout.draw()
        return True

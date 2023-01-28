import pyglet
import time
from .TransitionalScreen import TransitionalScreen
from .CCScreenBG import CCScreenBG
from .CCScreenCB import CCScreenCB
from .CCScreenTimeLabel import CCScreenTimeLabel


class CharChoiceScreen:
    def __init__(self, window, endWindow, gameMediaPlayer,
                 gameMediaList, charChoiceMediaPlayer, pauseScreen):
        self._window = window
        self._endWindow = endWindow
        self._gameMediaPlayer = gameMediaPlayer
        self._gameMediaList = gameMediaList
        self._charChoiceMediaPlayer = charChoiceMediaPlayer
        self._pauseScreen = pauseScreen
        self._screenBatch = pyglet.graphics.Batch()
        self._nextScreen = TransitionalScreen(self._window, self._endWindow, self._gameMediaPlayer, self._gameMediaList,
                                              self._pauseScreen)
        self._state = 'choosing'
        self._BG = None
        self._charButtons = None
        self._seconds = 5

    def screenInit(self, gameInfo, charToChooseFrom):
        self._gameInfo = gameInfo
        self._charToChooseFrom = charToChooseFrom
        self._BG = CCScreenBG(self._window, self._gameInfo, self._screenBatch)
        self._charButtons = CCScreenCB(
            self._window,
            self._gameInfo,
            self._charToChooseFrom,
            self._screenBatch)
        self._topLeftTimer = CCScreenTimeLabel(self._window.width // (4 * (self._gameInfo.playerCnt + 1)),
                                               self._window, self._gameInfo, self._screenBatch, color=(255, 255, 255, 255))
        self._topRightTimer = CCScreenTimeLabel(((4 * self._gameInfo.playerCnt + 3) * self._window.width) // (4 * (self._gameInfo.playerCnt + 1)),
                                                self._window, self._gameInfo, self._screenBatch, color=(255, 255, 255, 255))
        self._pauseScreen.setParent(self)
        self._charChoiceMediaPlayer.play()
        self._curPlayer = 0
        self._curResult = None
        self._chosenCharacters = list()
        self._chosenCharInfo = list()
        self.screenContinue()

    def screenContinue(self):
        self._window.push_handlers(on_key_press=self._onKeyPress, on_mouse_press=self._onMousePress, on_draw=self._onDraw,
                                   on_mouse_motion=self._onMouseMotion)
        self._timeval = time.time()
        pyglet.clock.schedule_interval(self._checkResultSchedulded, 1 / 30)

    def _screenEnd(self):
        self._window.pop_handlers()
        pyglet.clock.unschedule(self._checkResultSchedulded)
        self._charChoiceMediaPlayer.pause()
        self._gameInfo.chosenChars = self._chosenCharacters
        self._nextScreen.screenInit(self._gameInfo)

    def _changeToWaitState(self):
        self._state = 'waiting'
        self._curSecond = 0.0
        curPlayer = 0
        while curPlayer < self._gameInfo.playerCnt:
            self._charButtons.chooseButton(
                self._chosenCharInfo[curPlayer][0],
                self._chosenCharInfo[curPlayer][1])
            curPlayer += 1
        self._topLeftTimer.turnOn(self._seconds)
        self._topRightTimer.turnOn(self._seconds)
        self._timeval = time.time()

    def _checkResultSchedulded(self, dt):
        if self._state == 'waiting':
            self._onDraw()
            return None
        if self._curResult is not None:
            self._chosenCharacters.append(self._curResult)
            self._curResult = None
            self._curPlayer += 1
        if self._curPlayer == self._gameInfo.playerCnt:
            self._changeToWaitState()
            return None
        if not self._gameInfo.players[self._curPlayer].choosesCharacterInteractivly(
        ):
            curResult = self._gameInfo.players[self._curPlayer].chooseChar(
                self._gameInfo, self._charToChooseFrom, self._curPlayer)
            self._chosenCharacters.append(curResult[0])
            self._chosenCharInfo.append([self._curPlayer, curResult[1]])
            self._curPlayer += 1

    def _onKeyPress(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self._window.pop_handlers()
            pyglet.clock.unschedule(self._checkResultSchedulded)
            self._pauseScreen.pause()
        return True

    def _onMousePress(self, x, y, button, modifiers):
        if self._state == 'waiting':
            return True
        if self._curResult is None:
            curResult = self._charButtons.onMousePressRoutine(
                x, y, button, modifiers, self._curPlayer)
            if curResult is not None:
                self._curResult = curResult[0]
                self._chosenCharInfo.append([self._curPlayer, curResult[1]])
        return True

    def _onDraw(self):
        if self._state == 'waiting':
            newTimeval = time.time()
            curTimeDiff = newTimeval - self._timeval
            self._timeval = newTimeval
            self._curSecond += curTimeDiff
            if self._curSecond >= 1.0:
                self._curSecond = 0.0
                self._seconds -= 1
                if self._seconds == 0:
                    self._screenEnd()
                    return True
                self._topLeftTimer.countDown()
                self._topRightTimer.countDown()
        self._window.clear()
        self._screenBatch.draw()
        return True

    def _onMouseMotion(self, x, y, dx, dy):
        self._charButtons.onMouseMotionRoutine(x, y, dx, dy)

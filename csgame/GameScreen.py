import pyglet
import time
from .GSPlayerInfoRibbon import GSPlayerInfoRibbon
from .LowerRibbon import LowerRibbon
from .GSUpperRibbon import GSUpperRibbon
from .renderers.FieldRenderer import FieldRenderer
from .renderers.FRBasic import FRBasic
from .renderers.FRSimpleImage import FRSimpleImage


class GameScreen:
    def __init__(self, window, parent, gamePlayer,
                 pauseScreen, gameInfo, gamePosition):
        self._window = window
        self._parent = parent
        self._gamePlayer = gamePlayer
        self._pauseScreen = pauseScreen
        self._gameInfo = gameInfo
        self._gamePosition = gamePosition
        self._screenBatch = pyglet.graphics.Batch()
        self._FirstPlayerInfoRibbon = GSPlayerInfoRibbon(
            self._gamePosition, self._gameInfo.players[0], self._gameInfo.chosenChars[0],
            0, 0,
            self._window.width // 6, self._window.height,
            self._screenBatch, 5,
            (255, 192, 203), (255, 255, 0),
            (0, 200, 100), 5, 'right', 9
        )
        self._SecondPlayerInfoRibbon = GSPlayerInfoRibbon(
            self._gamePosition, self._gameInfo.players[1], self._gameInfo.chosenChars[1],
            (5 * self._window.width) // 6, 0,
            self._window.width // 6, self._window.height,
            self._screenBatch, 5,
            (255, 192, 203), (255, 255, 0),
            (0, 255, 127), 5, 'left', 9
        )
        self._lowerRibbon = LowerRibbon(
            self._window.width // 6, 0, (2 *
                                         self._window.width) // 3, (self._window.height) // 90,
            (0, 128, 0), self._screenBatch, 5
        )
        self._upperRibbon = GSUpperRibbon(
            self._gameInfo, self._window.width // 6, (9 *
                                                      self._window.height) // 10,
            (2 * self._window.width) // 3, self._window.height // 10,
            self._screenBatch, 5, 5, (0, 128, 0), 60
        )
        self._curSecond = 0.0
        self._listOfFieldRenderers = [FRBasic(
            self._window.width // 6, self._window.height // 90, (
                2 * self._window.width) // 3, (8 * self._window.height) // 9,
            self._gameInfo, self._gamePosition, self._screenBatch, 0, 3, (
                255, 255, 255), (255, 255, 255), 5, (150, 150, 150),
            (148, 0, 211)
        ), FRSimpleImage(
            self._window.width // 6, self._window.height // 90, (
                2 * self._window.width) // 3, (8 * self._window.height) // 9,
            self._gameInfo, self._gamePosition, self._screenBatch, 0, (
                255, 255, 255), 5, (150, 150, 150), (148, 0, 211)
        )]
        self._curRendererIndex = 0
        self._rendererCnt = len(self._listOfFieldRenderers)
        self._listOfFieldRenderers[self._curRendererIndex].turnOn()
        self._fieldCellTypesNums = self._gamePosition.field.getFieldCellTypesNums()

    def screenInit(self):
        self._pauseScreen.setParent(self)
        self.screenContinue()

    def screenContinue(self):
        self._window.push_handlers(on_key_press=self._onKeyPress, on_mouse_press=self._onMousePress, on_draw=self._onDraw,
                                   on_mouse_motion=self._onMouseMotion)
        if not self._gamePlayer.isPlaying():
            self._gamePlayer.play()
        self._timeval = time.time()
        pyglet.clock.schedule_interval(self._playerCheckScheduled, 1)
        pyglet.clock.schedule_interval(self._timerRoutine, 1 / 30)
        pyglet.clock.schedule_interval(self._noninteractivePlayerTurn, 1)

    def _screenEnd(self):
        self._window.pop_handlers()
        pyglet.clock.unschedule(self._playerCheckScheduled)
        pyglet.clock.unschedule(self._timerRoutine)
        pyglet.clock.unschedule(self._noninteractivePlayerTurn)
        self._gameInfo.addGameResults(self._gamePosition.getGameResults())
        self._gameInfo.currentGameNum += 1
        self._parent.screenContinue()

    def _playerCheckScheduled(self, dt):
        self._gamePlayer.checkPlayingSource()

    def _noninteractivePlayerTurn(self, dt):
        curPlayer = self._gameInfo.players[self._gamePosition.curPlayer]
        if not self._gameInfo.players[self._gamePosition.curPlayer].makesTurnsInteractivly(
        ):
            decision = curPlayer.takeCaptureDecision(
                self._gameInfo, self._gamePosition, self._gamePosition.curPlayer)
            if not self._gamePosition.workWithInput(decision):
                raise Exception("AI input error")
                return None
            self._onGameChange()

    def _timerRoutine(self, dt):
        if self._gamePosition.phase == "Playing":
            newTimeval = time.time()
            curTimeDiff = newTimeval - self._timeval
            self._timeval = newTimeval
            self._curSecond += curTimeDiff
            if self._curSecond >= 1.0:
                self._curSecond = 0.0
                self._upperRibbon.countDown()
                if self._upperRibbon.getCurTime() == 0:
                    self._gamePosition.makeRandomFullTurn()
                    if self._gamePosition.playerWasChangedWhenPlaying():
                        self._upperRibbon.setMaxTime()
                    self._listOfFieldRenderers[self._curRendererIndex].onChangeRoutine(
                    )
                self._onDraw()

    def _onPhaseChange(self):
        self._upperRibbon.setMaxTime()
        if self._gamePosition.phase == "Playing":
            self._timeval = time.time()
            self._gamePosition.phaseChangeToPlaying()

    def _onGameChange(self):
        if self._gamePosition.phaseWasChanged():
            self._onPhaseChange()
        if self._gamePosition.playerWasChangedWhenPlaying():
            self._upperRibbon.setMaxTime()
        if self._gamePosition.checkFinished():
            self._screenEnd()
            return None
        self._FirstPlayerInfoRibbon.onGameChange(
            self._gameInfo.chosenChars[0], self._gamePosition, 0)
        self._SecondPlayerInfoRibbon.onGameChange(
            self._gameInfo.chosenChars[1], self._gamePosition, 1)
        self._listOfFieldRenderers[self._curRendererIndex].onChangeRoutine()
        self._onDraw()

    def _onKeyPress(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self._window.pop_handlers()
            pyglet.clock.unschedule(self._playerCheckScheduled)
            pyglet.clock.unschedule(self._timerRoutine)
            pyglet.clock.unschedule(self._noninteractivePlayerTurn)
            self._gamePlayer.pause()
            self._pauseScreen.pause()
        return True

    def _onMousePress(self, x, y, button, modifiers):
        if self._upperRibbon.checkMouseOnChangeRendererButton(x, y):
            self._listOfFieldRenderers[self._curRendererIndex].turnOff()
            self._curRendererIndex += 1
            if self._curRendererIndex == self._rendererCnt:
                self._curRendererIndex = 0
            self._listOfFieldRenderers[self._curRendererIndex].turnOn()
            self._listOfFieldRenderers[self._curRendererIndex].onChangeRoutine(
            )
            self._onDraw()
            return True
        if self._gameInfo.players[self._gamePosition.curPlayer].makesTurnsInteractivly(
        ):
            resultFieldCellCoord = self._listOfFieldRenderers[self._curRendererIndex].findCellCoord(
                x, y)
            if resultFieldCellCoord is not None:
                if self._gamePosition.phase == "Playing":
                    if self._gamePosition.checkOwned(resultFieldCellCoord):
                        self._gamePosition.currentFromCell = resultFieldCellCoord
                        self._listOfFieldRenderers[self._curRendererIndex].onChangeRoutine(
                        )
                        self._onDraw()
                        return True
                    if self._gamePosition.currentFromCell is not None and self._gamePosition.workWithInput([
                       self._gamePosition.currentFromCell, resultFieldCellCoord]):
                        self._onGameChange()
                    return True
                elif self._gamePosition.phase == "Choosing start cells":
                    if self._gamePosition.workWithInput(resultFieldCellCoord):
                        self._onGameChange()
                    return True
        return True

    def _activePlayerColorRoutine(self):
        if self._gamePosition.curPlayer == 0:
            self._FirstPlayerInfoRibbon.turnOnActiveColor()
            self._SecondPlayerInfoRibbon.turnOnPassiveColor()
        elif self._gamePosition.curPlayer == 1:
            self._FirstPlayerInfoRibbon.turnOnPassiveColor()
            self._SecondPlayerInfoRibbon.turnOnActiveColor()
        else:
            self._FirstPlayerInfoRibbon.turnOnPassiveColor()
            self._SecondPlayerInfoRibbon.turnOnPassiveColor()

    def _onDraw(self):
        self._activePlayerColorRoutine()
        self._window.clear()
        self._screenBatch.draw()
        return True

    def _onMouseMotion(self, x, y, dx, dy):
        resultFieldCellCoord = self._listOfFieldRenderers[self._curRendererIndex].findCellCoord(
            x, y)
        if resultFieldCellCoord is not None:
            curCellType = self._gameInfo.cellTypes[self._fieldCellTypesNums[
                resultFieldCellCoord[0], resultFieldCellCoord[1]]]
            if self._upperRibbon.changeCellTypeInfo(curCellType):
                self._onDraw()
        else:
            if self._upperRibbon.changeCellTypeInfo(None):
                self._onDraw()

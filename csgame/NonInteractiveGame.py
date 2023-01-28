from .GameInfo import GameInfo
from .GamePosition import GamePosition
from .fgenerators.FieldGen import FieldGen
from .fgenerators.FieldGenRand import FieldGenRand
from .scgenerators.StartCellGen import StartCellGen
from .scgenerators.StartCellGenRand import StartCellGenRand


class NonInteractiveGame:
    def __init__(self, gameInfo, chosenChars):
        self._gameInfo = gameInfo
        for player in self._gameInfo.players:
            if player.makesTurnsInteractivly():
                raise Exception(
                    "NonInteractiveGame class works only with non-interactive Players.")
        self._gameInfo.chosenChars = chosenChars
        self._fieldGen = FieldGenRand()
        self._startCellGen = StartCellGenRand()

    def play(self):
        while self._gameInfo.currentGameNum < self._gameInfo.gameCnt:
            self._gameInfo.rememberChangableData()
            gameRes = self._playGame()
            self._gameInfo.addGameResults(gameRes)
            self._gameInfo.currentGameNum += 1
            self._gameInfo.restoreChangableData()
        return self._gameInfo.currentResults

    def _playGame(self):
        self._gamePosition = GamePosition(
            self._gameInfo, self._fieldGen, self._startCellGen)
        while True:
            if self._gamePosition.phaseWasChanged():
                self._onPhaseChange()
            if self._gamePosition.playerWasChangedWhenPlaying():
                self._onPlayerChange()
            if self._gamePosition.checkFinished():
                return self._gamePosition.getGameResults()
            self._captureDecision()

    def _captureDecision(self):
        curPlayer = self._gameInfo.players[self._gamePosition.curPlayer]
        decision = curPlayer.takeCaptureDecision(
            self._gameInfo, self._gamePosition, self._gamePosition.curPlayer)
        if not self._gamePosition.workWithInput(decision):
            raise Exception("AI input error")

    def _onPhaseChange(self):
        if self._gamePosition.phase == "Playing":
            self._gamePosition.phaseChangeToPlaying()

    def _onPlayerChange(self):
        return None

from .Character import Character


class Mirror(Character):
    def __init__(self, iconFile=None):
        super().__init__(iconFile)
        self._name = "Mirror"
        self._setDescriptionAndRules()
        self._cellCaptureCnt = 1

    def isHoly(self):
        return True

    def getPlayerTurnSequencePolicy(self):
        return "common"

    def _recalcCellCaptureCnt(self, gamePosition):
        self._cellCaptureCnt = self._basicCellCaptureCnt(gamePosition) + 1

    def onGameStart(self, gamePosition):
        return None

    def onTurnEndRoutine(self, gamePosition):
        return None

    def afterPlayersTurnRoutine(self, gamePosition, prevPlayer):
        prevPlayerChar = gamePosition.gameInfo.chosenChars[prevPlayer]
        gamePosition.gameInfo.chosenChars[prevPlayer] = gamePosition.gameInfo.chosenChars[gamePosition.curPlayer]
        gamePosition.gameInfo.chosenChars[gamePosition.curPlayer] = prevPlayerChar

    def onGameEnd(self, gamePosition):
        self._cellCaptureCnt = 1

    def generateCharacterCapturesFromCell(
            self, gamePosition, cell, capture_points_check=True):
        return self._generateBasicCapturesFromCell(
            gamePosition, cell, capture_points_check=capture_points_check)

    def _rightAfterCaptureInsideChange(self, gamePosition, captureData):
        return None

    def getCharGameDataText(self, gamePosition, playerNum):
        return self._getBasicCharGameDataText(gamePosition, playerNum)

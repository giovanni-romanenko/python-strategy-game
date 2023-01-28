from .Character import Character

# unfinished character


class AdmiralTriangle(Character):
    def __init__(self, iconFile=None):
        super().__init__(iconFile)
        self._name = "Admiral Triangle"
        self._setDescriptionAndRules()
        self._cellCaptureCnt = 1
        self._level = 1

    def isHoly(self):
        return True

    def getPlayerTurnSequencePolicy(self):
        return "common"

    def _recalcCellCaptureCnt(self, gamePosition):
        pass

    def onGameStart(self, gamePosition):
        return None

    def onTurnEndRoutine(self, gamePosition):
        return None

    def afterPlayersTurnRoutine(self, gamePosition, prevPlayer):
        return None

    def onGameEnd(self, gamePosition):
        self._cellCaptureCnt = 1
        self._level = 1

    def generateCharacterCapturesFromCell(
            self, gamePosition, cell, capture_points_check=True):
        pass  # todo

    def _rightAfterCaptureInsideChange(self, gamePosition, captureData):
        pass

    def getCharGameDataText(self, gamePosition, playerNum):
        pass

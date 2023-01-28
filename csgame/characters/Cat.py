import words
from .Character import Character


class Cat(Character):
    def __init__(self, iconFile=None):
        super().__init__(iconFile)
        self._name = "Cat"
        self._setDescriptionAndRules()
        self._cellCaptureCnt = 1
        self._combo = 0
        self._comboDrop = True

    def isHoly(self):
        return False

    def getPlayerTurnSequencePolicy(self):
        return "common"

    def _recalcCellCaptureCnt(self, gamePosition):
        self._cellCaptureCnt = self._basicCellCaptureCnt(
            gamePosition) + max(0, self._combo - 1) + 1

    def onGameStart(self, gamePosition):
        return None

    def onTurnEndRoutine(self, gamePosition):
        if self._comboDrop:
            self._combo = 0
        self._comboDrop = True

    def afterPlayersTurnRoutine(self, gamePosition, prevPlayer):
        return None

    def onGameEnd(self, gamePosition):
        self._cellCaptureCnt = 1
        self._combo = 0
        self._comboDrop = True

    def generateCharacterCapturesFromCell(
            self, gamePosition, cell, capture_points_check=True):
        return self._generateBasicCapturesFromCell(
            gamePosition, cell, capture_points_check=capture_points_check)

    def _rightAfterCaptureInsideChange(self, gamePosition, captureData):
        fieldCellTypeNums = gamePosition.field.getFieldCellTypesNums()
        toCellTypeNum = fieldCellTypeNums[captureData[1][0]][captureData[1][1]]
        toCellTypeName = gamePosition.gameInfo.cellTypes[toCellTypeNum].getName(
        )
        if toCellTypeName == "Blood":
            self._comboDrop = False
            self._combo += 1
            if self._combo >= 2:
                gamePosition.curPlayerCellCaptureCnt += 1

    def getCharGameDataText(self, gamePosition, playerNum):
        result = self._getBasicCharGameDataText(gamePosition, playerNum) + "\n"
        result += words.word.combo() + ": " + str(self._combo)
        return result

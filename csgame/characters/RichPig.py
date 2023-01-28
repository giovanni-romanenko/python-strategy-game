from .Character import Character


class RichPig(Character):
    def __init__(self, iconFile=None):
        super().__init__(iconFile)
        self._name = "Rich Pig"
        self._setDescriptionAndRules()
        self._cellCaptureCnt = 1

    def isHoly(self):
        return False

    def getPlayerTurnSequencePolicy(self):
        return "common"

    def _recalcCellCaptureCnt(self, gamePosition):
        self._cellCaptureCnt = (
            self._basicCellCaptureCnt(gamePosition) + min(
                gamePosition.cntCellsOfGivenCellType("Bank"),
                gamePosition.cntCellsOfGivenCellType("Pigs")
            )
        ) + 1

    def onGameStart(self, gamePosition):
        return None

    def onTurnEndRoutine(self, gamePosition):
        return None

    def afterPlayersTurnRoutine(self, gamePosition, prevPlayer):
        return None

    def onGameEnd(self, gamePosition):
        self._cellCaptureCnt = 1

    def generateCharacterCapturesFromCell(
            self, gamePosition, cell, capture_points_check=True):
        return self._generateBasicCapturesFromCell(
            gamePosition, cell, capture_points_check=capture_points_check)

    def _rightAfterCaptureInsideChange(self, gamePosition, captureData):
        fieldCellTypeNums = gamePosition.field.getFieldCellTypesNums()
        toCellTypeNum = fieldCellTypeNums[captureData[1][0]][captureData[1][1]]
        toCellTypeName = gamePosition.gameInfo.cellTypes[toCellTypeNum].getName(
        )
        if toCellTypeName != "Bank" and toCellTypeName != "Pigs":
            return None
        bankCnt = gamePosition.cntCellsOfGivenCellType("Bank")
        pigsCnt = gamePosition.cntCellsOfGivenCellType("Pigs")
        oldMin = min(bankCnt, pigsCnt)
        if toCellTypeName == "Bank":
            bankCnt += 1
        elif toCellTypeName == "Pigs":
            pigsCnt += 1
        newMin = min(bankCnt, pigsCnt)
        if newMin > oldMin:
            gamePosition.curPlayerCellCaptureCnt += 1

    def getCharGameDataText(self, gamePosition, playerNum):
        return self._getBasicCharGameDataText(gamePosition, playerNum)

from .Character import Character


class Yin(Character):
    def __init__(self, iconFile=None):
        super().__init__(iconFile)
        self._name = "Yin"
        self._setDescriptionAndRules()
        self._cellCaptureCnt = 1

    def isHoly(self):
        return False

    def getPlayerTurnSequencePolicy(self):
        return "common"

    def _recalcCellCaptureCnt(self, gamePosition):
        self._cellCaptureCnt = (
            self._basicCellCaptureCnt(gamePosition) + (min(
                gamePosition.cntCellsOfGivenCellType("Bog"),
                gamePosition.cntCellsOfGivenCellType("Dark")
            ) // 2)
        ) + 1

    def onGameStart(self, gamePosition):
        return None

    def onTurnEndRoutine(self, gamePosition):
        ownageData = gamePosition.ownageData
        fieldCellTypesNums = gamePosition.field.getFieldCellTypesNums()
        width = gamePosition.field.getWidth()
        height = gamePosition.field.getHeight()
        bogCellTypeNum = gamePosition.gameInfo.cellTypeNumByName["Bog"]
        darkCellTypeNum = gamePosition.gameInfo.cellTypeNumByName["Dark"]
        cellX = 0
        while cellX < width:
            cellY = 0
            while cellY < height:
                if ownageData[cellX][cellY] == gamePosition.curPlayer:
                    cellType = gamePosition.gameInfo.cellTypes[fieldCellTypesNums[cellX][cellY]]
                    if cellType.isWatery() and cellType.getName() != "Bog":
                        fieldCellTypesNums[cellX][cellY] = bogCellTypeNum
                    if (not cellType.isWatery()) and cellType.getName() != "Dark":
                        fieldCellTypesNums[cellX][cellY] = darkCellTypeNum
                cellY += 1
            cellX += 1

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
        if toCellTypeName != "Bog" and toCellTypeName != "Dark":
            return None
        bogCnt = gamePosition.cntCellsOfGivenCellType("Bog")
        darkCnt = gamePosition.cntCellsOfGivenCellType("Dark")
        oldMin = min(bogCnt, darkCnt)
        if toCellTypeName == "Bog":
            bogCnt += 1
        elif toCellTypeName == "Dark":
            darkCnt += 1
        newMin = min(bogCnt, darkCnt)
        if newMin // 2 > oldMin // 2:
            gamePosition.curPlayerCellCaptureCnt += 1

    def getCharGameDataText(self, gamePosition, playerNum):
        return self._getBasicCharGameDataText(gamePosition, playerNum)

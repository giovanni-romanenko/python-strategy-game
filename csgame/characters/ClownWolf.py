import numpy as np
from .Character import Character


class ClownWolf(Character):
    def __init__(self, iconFile=None):
        super().__init__(iconFile)
        self._name = "Clown-Wolf"
        self._setDescriptionAndRules()
        self._cellCaptureCnt = 1

    def isHoly(self):
        return False

    def getPlayerTurnSequencePolicy(self):
        return "common"

    def _recalcCellCaptureCnt(self, gamePosition):
        self._cellCaptureCnt = self._basicCellCaptureCnt(
            gamePosition) + (gamePosition.cntCellsOfGivenCellType("Blood") // 2) + 1

    def onGameStart(self, gamePosition):
        pigsCellTypeNum = gamePosition.gameInfo.cellTypeNumByName["Pigs"]
        bloodCellTypeNum = gamePosition.gameInfo.cellTypeNumByName["Blood"]
        fieldCellTypesNums = gamePosition.field.getFieldCellTypesNums()
        fieldCellTypesNums[fieldCellTypesNums ==
                           pigsCellTypeNum] = bloodCellTypeNum

    def onTurnEndRoutine(self, gamePosition):
        return None

    def afterPlayersTurnRoutine(self, gamePosition, prevPlayer):
        return None

    def onGameEnd(self, gamePosition):
        self._cellCaptureCnt = 1

    def generateCharacterCapturesFromCell(
            self, gamePosition, cell, capture_points_check=True):
        result = list()
        fieldCellTypesNums = gamePosition.field.getFieldCellTypesNums()
        curDiffX = -1
        while curDiffX <= 1:
            curDiffY = -1
            while curDiffY <= 1:
                toCell = [cell[0] + curDiffX, cell[1] + curDiffY]
                if (abs(curDiffX) + abs(curDiffY) == 1 and gamePosition.field.isOnField(toCell[0], toCell[1])
                        and gamePosition.ownageData[toCell[0]][toCell[1]] == -1):
                    curCellType = gamePosition.gameInfo.cellTypes[fieldCellTypesNums[toCell[0]][toCell[1]]]
                    if (curCellType.checkBasicCaptureIsPossible(gamePosition, cell, toCell, capture_points_check=capture_points_check)
                            or curCellType.getName() == "Forest"):
                        result.append([cell, toCell])
                curDiffY += 1
            curDiffX += 1
        return result

    def _rightAfterCaptureInsideChange(self, gamePosition, captureData):
        fieldCellTypeNums = gamePosition.field.getFieldCellTypesNums()
        toCellTypeNum = fieldCellTypeNums[captureData[1][0]][captureData[1][1]]
        toCellTypeName = gamePosition.gameInfo.cellTypes[toCellTypeNum].getName(
        )
        if toCellTypeName == "Blood":
            oldBloodCnt = gamePosition.cntCellsOfGivenCellType("Blood")
            if oldBloodCnt % 2 == 1:
                gamePosition.curPlayerCellCaptureCnt += 1
        if toCellTypeName == "Forest":
            gamePosition.curPlayerCellCaptureCnt += 2

    def getCharGameDataText(self, gamePosition, playerNum):
        return self._getBasicCharGameDataText(gamePosition, playerNum)

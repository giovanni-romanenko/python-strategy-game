from .Character import Character


class WaterBucket(Character):
    def __init__(self, iconFile=None):
        super().__init__(iconFile)
        self._name = "Water Bucket"
        self._setDescriptionAndRules()
        self._cellCaptureCnt = 1

    def isHoly(self):
        return False

    def getPlayerTurnSequencePolicy(self):
        return "common"

    def _recalcCellCaptureCnt(self, gamePosition):
        self._cellCaptureCnt = self._basicCellCaptureCnt(gamePosition) + 1

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
        result = list()
        fieldCellTypesNums = gamePosition.field.getFieldCellTypesNums()
        cellType = gamePosition.gameInfo.cellTypes[fieldCellTypesNums[cell[0]][cell[1]]]
        curDiffX = -2
        while curDiffX <= 2:
            curDiffY = -2
            while curDiffY <= 2:
                toCell = [cell[0] + curDiffX, cell[1] + curDiffY]
                absSum = abs(curDiffX) + abs(curDiffY)
                if absSum == 1:
                    if (gamePosition.field.isOnField(toCell[0], toCell[1])
                            and gamePosition.ownageData[toCell[0]][toCell[1]] == -1):
                        curCellType = gamePosition.gameInfo.cellTypes[
                            fieldCellTypesNums[toCell[0]][toCell[1]]]
                        if (curCellType.checkBasicCaptureIsPossible(gamePosition, cell, toCell, capture_points_check=capture_points_check)
                                or curCellType.getName() == "Mountain"):
                            result.append([cell, toCell])
                elif absSum == 2:
                    if (gamePosition.field.isOnField(toCell[0], toCell[1])
                        and gamePosition.ownageData[toCell[0]][toCell[1]] == -1
                            and cellType.getName() == "Mountain"):
                        curCellType = gamePosition.gameInfo.cellTypes[
                            fieldCellTypesNums[toCell[0]][toCell[1]]]
                        if (curCellType.checkBasicCaptureIsPossible(gamePosition, cell, toCell, capture_points_check=capture_points_check)
                                or curCellType.getName() == "Mountain"):
                            result.append([cell, toCell])
                curDiffY += 1
            curDiffX += 1
        return result

    def _rightAfterCaptureInsideChange(self, gamePosition, captureData):
        return None

    def getCharGameDataText(self, gamePosition, playerNum):
        return self._getBasicCharGameDataText(gamePosition, playerNum)

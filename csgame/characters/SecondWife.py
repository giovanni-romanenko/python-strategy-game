from .Character import Character


class SecondWife(Character):
    def __init__(self, iconFile=None):
        super().__init__(iconFile)
        self._name = "Second Wife"
        self._setDescriptionAndRules()
        self._cellCaptureCnt = 1

    def isHoly(self):
        return False

    def getPlayerTurnSequencePolicy(self):
        return "always second"

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
        result = self._generateBasicCapturesFromCell(
            gamePosition, cell, capture_points_check=capture_points_check)
        fieldCellTypesNums = gamePosition.field.getFieldCellTypesNums()
        curDiffX = -1
        while curDiffX <= 1:
            curDiffY = -1
            while curDiffY <= 1:
                toCell = [cell[0] + curDiffX, cell[1] + curDiffY]
                if (abs(curDiffX) + abs(curDiffY) == 1 and gamePosition.field.isOnField(toCell[0], toCell[1])
                    and gamePosition.ownageData[toCell[0]][toCell[1]] != gamePosition.curPlayer
                        and gamePosition.ownageData[toCell[0]][toCell[1]] != -1):
                    curCellType = gamePosition.gameInfo.cellTypes[fieldCellTypesNums[toCell[0]][toCell[1]]]
                    if (curCellType.getName() == "Bank"
                            and curCellType.checkBasicCaptureIsPossible(gamePosition, cell, toCell, capture_points_check=capture_points_check)):
                        result.append([cell, toCell])
                curDiffY += 1
            curDiffX += 1
        return result

    def _rightAfterCaptureInsideChange(self, gamePosition, captureData):
        return None

    def getCharGameDataText(self, gamePosition, playerNum):
        return self._getBasicCharGameDataText(gamePosition, playerNum)

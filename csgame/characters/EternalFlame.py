from .Character import Character


class EternalFlame(Character):
    def __init__(self, iconFile=None):
        super().__init__(iconFile)
        self._name = "Eternal Flame"
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
        ownageData = gamePosition.ownageData
        fieldCellTypesNums = gamePosition.field.getFieldCellTypesNums()
        width = gamePosition.field.getWidth()
        height = gamePosition.field.getHeight()
        finished = False
        while not finished:
            finished = True
            cellX = 0
            while cellX < width:
                cellY = 0
                while cellY < height:
                    if (ownageData[cellX][cellY] == gamePosition.curPlayer
                            and gamePosition.gameInfo.cellTypes[fieldCellTypesNums[cellX][cellY]].getName() == "Fire"):
                        if self._captureNeighbours(
                                gamePosition, [cellX, cellY]):
                            finished = False
                    cellY += 1
                cellX += 1

    def _captureNeighbours(self, gamePosition, cell):
        result = False
        curDiffX = -1
        while curDiffX <= 1:
            curDiffY = -1
            while curDiffY <= 1:
                toCell = [cell[0] + curDiffX, cell[1] + curDiffY]
                if gamePosition.gameMaster.capture(
                        gamePosition, [cell, toCell], capture_points_check=False):
                    result = True
                curDiffY += 1
            curDiffX += 1
        return result

    def afterPlayersTurnRoutine(self, gamePosition, prevPlayer):
        return None

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

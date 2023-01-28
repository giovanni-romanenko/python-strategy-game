import pyglet
import words
import numpy as np


class Character:
    def __init__(self, iconFile=None):
        self._iconFile = iconFile
        self._iconImage = None
        self._iconSprite = None
        self._name = None
        self._description = None
        self._rulesDescription = None
        self._cellCaptureCnt = None
        self._makeSprite()

    def _makeSprite(self):
        if self._iconFile is not None:
            self._iconImage = pyglet.resource.image(self._iconFile)
            self._iconSprite = pyglet.sprite.Sprite(self._iconImage)
        else:
            self._iconImage = None
            self._iconSprite = None

    def _setDescriptionAndRules(self):
        self._description = words.word.characterDescription(self._name)
        self._rulesDescription = words.word.characterRulesDescription(
            self._name)

    def setIcon(self, x, y, width, height, batch, group):
        self._iconSprite.update(x=x, y=y, scale_x=self._iconSprite.scale_x * (width / self._iconSprite.width),
                                scale_y=self._iconSprite.scale_y * (height / self._iconSprite.height))
        self._iconSprite.batch = batch
        self._iconSprite.group = group

    def getSprite(self):
        return self._iconSprite

    def getName(self):
        return self._name

    def isHoly(self):
        pass

    def getCellCaptureCnt(self, gamePosition):
        self._recalcCellCaptureCnt(gamePosition)
        return self._cellCaptureCnt

    def _recalcCellCaptureCnt(self, gamePosition):
        pass

    def _basicCellCaptureCnt(self, gamePosition):
        return gamePosition.cntCellsOfGivenCellType("Bank") // 2

    def getPlayerTurnSequencePolicy(self):
        pass

    def onGameStart(self, gamePosition):
        pass

    def onTurnEndRoutine(self, gamePosition):
        pass

    def afterPlayersTurnRoutine(self, gamePosition, prevPlayer):
        pass

    def onGameEnd(self, gamePosition):
        pass

    def _generateBasicCapturesFromCell(
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
                    if curCellType.checkBasicCaptureIsPossible(
                            gamePosition, cell, toCell, capture_points_check=capture_points_check):
                        result.append([cell, toCell])
                curDiffY += 1
            curDiffX += 1
        return result

    def generateCharacterCapturesFromCell(
            self, gamePosition, cell, capture_points_check=True):
        pass

    def _rightAfterCaptureInsideChange(self, gamePosition, captureData):
        pass

    def onCapture(self, gamePosition, captureData):
        fieldCellTypesNums = gamePosition.field.getFieldCellTypesNums()
        toCellTypeNum = fieldCellTypesNums[captureData[1]
                                           [0]][captureData[1][1]]
        toCellType = gamePosition.gameInfo.cellTypes[toCellTypeNum]
        toCellType.onCaptureTo(gamePosition, captureData)
        toCellTypeNum = fieldCellTypesNums[captureData[1]
                                           [0]][captureData[1][1]]
        toCellType = gamePosition.gameInfo.cellTypes[toCellTypeNum]
        toCellType.onCaptureToPhaseTwo(gamePosition, captureData)
        self._rightAfterCaptureInsideChange(gamePosition, captureData)

    def getCharGameDataText(self, gamePosition, playerNum):
        pass

    def _getBasicCharGameDataText(self, gamePosition, playerNum):
        curGameChar = gamePosition.gameInfo.chosenChars[gamePosition.curPlayer]
        result = words.word.totalCaptured() + ": "
        if gamePosition.phase == "Playing":
            totalCapturedCnt = np.count_nonzero(
                gamePosition.ownageData == playerNum)
            result += str(totalCapturedCnt)
        else:
            result += "0"
        result += "\n" + words.word.capturePnts() + ": "
        if gamePosition.phase == "Playing" and self is curGameChar:
            result += str(gamePosition.curPlayerCellCaptureCnt)
        else:
            result += "0"
        return result

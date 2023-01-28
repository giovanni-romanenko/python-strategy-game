
class GameMaster:
    def __init__(self):
        pass

    def generateAllCaptures(self, gamePosition):
        result = list()
        width = gamePosition.field.getWidth()
        height = gamePosition.field.getHeight()
        cellX = 0
        while cellX < width:
            cellY = 0
            while cellY < height:
                result.extend(
                    self._generateAllCapturesFromCell(
                        gamePosition, [
                            cellX, cellY]))
                cellY += 1
            cellX += 1
        return result

    def _generateAllCapturesFromCell(
            self, gamePosition, cell, capture_points_check=True):
        cellPlayerNum = gamePosition.ownageData[cell[0]][cell[1]]
        if cellPlayerNum != gamePosition.curPlayer:
            return list()
        cellCharacter = gamePosition.gameInfo.chosenChars[cellPlayerNum]
        return cellCharacter.generateCharacterCapturesFromCell(
            gamePosition, cell, capture_points_check=capture_points_check)

    def capture(self, gamePosition, captureData, capture_points_check=True):
        if not captureData in self._generateAllCapturesFromCell(
           gamePosition, captureData[0], capture_points_check=capture_points_check
           ):
            return False
        cellPlayerNum = gamePosition.ownageData[captureData[0]
                                                [0]][captureData[0][1]]
        cellCharacter = gamePosition.gameInfo.chosenChars[cellPlayerNum]
        cellCharacter.onCapture(gamePosition, captureData)
        gamePosition.ownageData[captureData[1][0]
                                ][captureData[1][1]] = gamePosition.curPlayer
        if capture_points_check:
            gamePosition.curPlayerCellCaptureCnt -= 1
        return True

    def canCapture(self, gamePosition):
        width = gamePosition.field.getWidth()
        height = gamePosition.field.getHeight()
        cellX = 0
        while cellX < width:
            cellY = 0
            while cellY < height:
                if self._generateAllCapturesFromCell(
                        gamePosition, [cellX, cellY]) != list():
                    return True
                cellY += 1
            cellX += 1
        return False

    def onGameStart(self, gamePosition):
        for character in gamePosition.gameInfo.chosenChars:
            character.onGameStart(gamePosition)

    def onTurnEnd(self, gamePosition):
        curChar = gamePosition.gameInfo.chosenChars[gamePosition.curPlayer]
        curChar.onTurnEndRoutine(gamePosition)

    def afterPlayersTurn(self, gamePosition, prevPlayer):
        curChar = gamePosition.gameInfo.chosenChars[gamePosition.curPlayer]
        curChar.afterPlayersTurnRoutine(gamePosition, prevPlayer)

    def onGameEnd(self, gamePosition):
        for character in gamePosition.gameInfo.chosenChars:
            character.onGameEnd(gamePosition)

    def applyPermPolicies(self, gamePosition):
        i = 0
        for character in gamePosition.gameInfo.chosenChars:
            if character.getPlayerTurnSequencePolicy(
            ) == "always second" and gamePosition.playersPerm[1] != i:
                playerIndex = gamePosition.playersPerm.index(i)
                gamePosition.playersPerm[playerIndex] = gamePosition.playersPerm[1]
                gamePosition.playersPerm[1] = i
            i += 1
        gamePosition.curPlayer = gamePosition.playersPerm[gamePosition.curPlayerCnt]

import copy
import numpy as np


class GameInfo:
    def __init__(self, players, playerOnScreen, characters, charChoiceList, gameCnt, gamesSizes, playersPermutations,
                 winPoints, cellTypes, startCellCounts):
        self.playerCnt = len(players)
        self.players = players
        self.playerOnScreen = playerOnScreen
        self.characters = characters
        self.charChoiceList = charChoiceList
        self.gameCnt = gameCnt
        self.gamesSizes = gamesSizes
        self.playersPerms = playersPermutations
        self.winPoints = winPoints
        self.cellTypes = cellTypes
        self.cellTypesCnt = len(self.cellTypes)
        self.cellTypeNumByName = dict()
        i = 0
        while i < self.cellTypesCnt:
            self.cellTypeNumByName[self.cellTypes[i].getName()] = i
            i += 1
        self.startCellCounts = startCellCounts
        self.chosenChars = None
        self.currentGameNum = 0
        self.currentResults = np.full(self.playerCnt, 0)
        self._charsBeforeGame = None

    def addGameResults(self, results):
        self.currentResults += results

    def rememberChangableData(self):
        self._charsBeforeGame = copy.copy(self.chosenChars)

    def restoreChangableData(self):
        if self._charsBeforeGame is not None:
            self.chosenChars = self._charsBeforeGame
            self._charsBeforeGame = None

    def getCopy(self):
        gameInfoCopy = copy.copy(self)
        gameInfoCopy.chosenChars = copy.copy(self.chosenChars)
        return gameInfoCopy

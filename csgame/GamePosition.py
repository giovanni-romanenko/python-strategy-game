import copy
import random
import numpy as np
from .GameMaster import GameMaster


class GamePosition:
    def __init__(self, gameInfo, fieldGen, startCellGen):
        self.gameInfo = gameInfo
        self._maxActiveTurns = 50
        self._maxActiveTurns += 1
        self.playersPerm = copy.copy(
            gameInfo.playersPerms[gameInfo.currentGameNum])
        self.field = fieldGen.generateField(gameInfo)
        self.startCells = startCellGen.generateStartCells(gameInfo, self.field)
        self.phase = "Choosing start cells"
        self.ownageData = np.full(
            (self.field.getWidth(), self.field.getHeight()), -1)
        self.chosenStartCells = list()
        i = 0
        while i < self.gameInfo.playerCnt:
            self.chosenStartCells.append(None)
            i += 1
        self.currentFromCell = None
        self._phaseWasChanged = False
        self._playerWasChangedWhenPlaying = False
        self._gameFinished = False
        self.gameMaster = GameMaster()
        self.curPlayerCnt = 0
        self.curPlayer = self.playersPerm[self.curPlayerCnt]
        self.curPlayerCellCaptureCnt = None
        self.gameMaster.applyPermPolicies(self)

    def workWithInput(self, input) -> bool:
        startPhase = self.phase
        if self.phase == "Playing":
            if not self._workWithInputPlayingPhase(input):
                return False
        elif self.phase == "Choosing start cells":
            if not self._workWithInputChoosingPhase(input):
                return False
        if startPhase != self.phase:
            self._phaseWasChanged = True
        self.currentFromCell = None
        return True

    def _workWithInputChoosingPhase(self, input) -> bool:
        if not (input in self.startCells[self.curPlayer]):
            return False
        self.chosenStartCells[self.curPlayer] = input
        self._nextPlayer()
        if self.curPlayerCnt == 0:
            self.phase = "Playing"
        return True

    def _workWithInputPlayingPhase(self, input) -> bool:
        if not self.gameMaster.capture(self, input):
            return False
        if self.curPlayerCellCaptureCnt == 0:
            self._nextPlayer()
        self._goTillNextPlayerWhoCanMakeATurnPlayingPhase()
        return True

    def _goTillNextPlayerWhoCanMakeATurnPlayingPhase(self):
        if not self._playerWasChangedWhenPlaying and not self.gameMaster.canCapture(
                self):
            self._nextPlayer()
        startPlayerCnt = self.curPlayerCnt
        while not self.gameMaster.canCapture(self):
            self._nextPlayer()
            if self.curPlayerCnt == startPlayerCnt:
                self._gameFinished = True
                self.gameMaster.onGameEnd(self)
                return None
        self._maxActiveTurns -= 1
        if self._maxActiveTurns == 0:
            self._gameFinished = True
            self.gameMaster.onGameEnd(self)

    def phaseChangeToPlaying(self):
        if self.phase != "Playing":
            raise Exception(
                "Calling playing phase change routine, though phase was not changed.")
        curPlayer = 0
        for chosenStartCell in self.chosenStartCells:
            if chosenStartCell is not None:
                self.ownageData[chosenStartCell[0]
                                ][chosenStartCell[1]] = curPlayer
            curPlayer += 1
        self.gameMaster.onGameStart(self)
        self.curPlayerCellCaptureCnt = self.gameInfo.chosenChars[self.curPlayer].getCellCaptureCnt(
            self)
        self._goTillNextPlayerWhoCanMakeATurnPlayingPhase()

    def generateAllValidGameInput(self):
        if self.phase == "Playing":
            return self._generateAllValidPlayingPhaseInput()
        elif self.phase == "Choosing start cells":
            return self._generateAllValidChoosingPhaseInput()

    def _generateAllValidChoosingPhaseInput(self):
        return self.startCells[self.curPlayer]

    def _generateAllValidPlayingPhaseInput(self):
        return self.gameMaster.generateAllCaptures(self)

    def makeRandomFullTurn(self):
        if self.phase != "Playing":
            raise Exception("Calling random turn method in wrong phase.")
        while not self._playerWasChangedWhenPlaying:
            allPossibleInputs = self.generateAllValidGameInput()
            self.workWithInput(random.sample(allPossibleInputs, 1)[0])

    def getGameResults(self):
        gameResult = np.full(self.gameInfo.playerCnt, 0)
        allPlayersCountsVector = np.full(self.gameInfo.playerCnt, 0)
        ownageVector, countsVector = np.unique(
            self.ownageData, return_counts=True)
        i = 0
        for owner in ownageVector:
            if owner != -1:
                allPlayersCountsVector[owner] = countsVector[i]
            i += 1
        aPCVSortedIndex = np.argsort(allPlayersCountsVector)[::-1]
        winPoints = self.gameInfo.winPoints[self.gameInfo.currentGameNum]
        ileft, iright = 0, 0
        curSum = 0
        while iright < self.gameInfo.playerCnt:
            if allPlayersCountsVector[aPCVSortedIndex[ileft]
                                      ] != allPlayersCountsVector[aPCVSortedIndex[iright]]:
                curRes = curSum // (iright - ileft)
                while ileft < iright:
                    gameResult[aPCVSortedIndex[ileft]] = curRes
                    ileft += 1
                curSum = 0
            curSum += winPoints[iright]
            iright += 1
        curRes = curSum // (iright - ileft)
        while ileft < iright:
            gameResult[aPCVSortedIndex[ileft]] = curRes
            ileft += 1
        return gameResult

    def checkOwned(self, cell):
        if self.ownageData[cell[0]][cell[1]] == self.curPlayer:
            return True
        return False

    def _nextPlayer(self):
        if self.phase == "Playing":
            self.gameMaster.onTurnEnd(self)
        prevPlayer = self.curPlayer
        self.curPlayerCnt += 1
        if self.curPlayerCnt == self.gameInfo.playerCnt:
            self.curPlayerCnt = 0
        self.curPlayer = self.playersPerm[self.curPlayerCnt]
        if self.phase == "Playing":
            self._playerWasChangedWhenPlaying = True
            self.gameMaster.afterPlayersTurn(self, prevPlayer)
            self.curPlayerCellCaptureCnt = self.gameInfo.chosenChars[self.curPlayer].getCellCaptureCnt(
                self)

    def phaseWasChanged(self):
        if self._phaseWasChanged:
            self._phaseWasChanged = False
            return True
        return False

    def playerWasChangedWhenPlaying(self):
        if self._playerWasChangedWhenPlaying:
            self._playerWasChangedWhenPlaying = False
            return True
        return False

    def checkFinished(self):
        return self._gameFinished

    def cntCellsOfGivenCellType(self, cellTypeName):
        givenCTNum = self.gameInfo.cellTypeNumByName[cellTypeName]
        fieldCellTypesNums = self.field.getFieldCellTypesNums()
        return np.count_nonzero(
            (fieldCellTypesNums == givenCTNum) * (self.ownageData == self.curPlayer))

    def getDeepCopy(self, gameInfo):
        gameInfoCopy = self.gameInfo
        self.gameInfo = None
        dc = copy.deepcopy(self)
        dc.gameInfo = gameInfo
        self.gameInfo = gameInfoCopy
        return dc

import random
from .StartCellGen import StartCellGen


class StartCellGenRand(StartCellGen):
    def generateStartCells(self, gameInfo, field):
        curGame = gameInfo.currentGameNum
        generCnts = gameInfo.startCellCounts[curGame]
        toGenerateCnt = sum(generCnts)
        allCells = list()
        curX = 0
        while curX < field.getWidth():
            curY = 0
            while curY < field.getHeight():
                allCells.append([curX, curY])
                curY += 1
            curX += 1
        chosenCells = random.sample(allCells, toGenerateCnt)
        prevI = 0
        nextI = 0
        i = 0
        cnt = len(generCnts)
        res = list()
        while i < cnt:
            prevI = nextI
            nextI += generCnts[i]
            res.append(chosenCells[prevI:nextI])
            i += 1
        return res

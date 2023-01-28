import numpy as np
from ..Field import Field
from .FieldGen import FieldGen


class FieldGenRand(FieldGen):
    def generateField(self, gameInfo):
        fieldInfo = list()
        sizes = gameInfo.gamesSizes[gameInfo.currentGameNum]
        width = sizes[0]
        height = sizes[1]
        fieldInfo.append(width)
        fieldInfo.append(height)
        cellTypesCnt = gameInfo.cellTypesCnt
        fieldCellTypeNums = np.random.randint(
            cellTypesCnt, size=(width, height))
        fieldInfo.append(fieldCellTypeNums)
        return Field(gameInfo, fieldInfo)

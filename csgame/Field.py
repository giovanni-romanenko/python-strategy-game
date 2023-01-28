import numpy as np


class Field:
    def __init__(self, gameInfo, fieldInfo):
        self._width = fieldInfo[0]
        self._height = fieldInfo[1]
        self._fieldCellTypes = fieldInfo[2]

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def getFieldCellTypesNums(self):
        return self._fieldCellTypes

    def setFieldCellTypesNums(self, field):
        self._fieldCellTypes = field

    def isOnField(self, x, y):
        if x >= 0 and x < self._width and y >= 0 and y < self._height:
            return True
        return False

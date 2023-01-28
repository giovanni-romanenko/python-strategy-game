

class FieldRenderer:
    def __init__(self, x, y, width, height, gameInfo,
                 gamePosition, batch, groupNum):
        """Uses ordered groups with indexes from [groupNum, groupNum+5)."""
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._gameInfo = gameInfo
        self._gamePosition = gamePosition
        self._batch = batch
        self._groupNum = groupNum

    def turnOn(self):
        pass

    def turnOff(self):
        pass

    def onChangeRoutine(self):
        pass

    def findCellCoord(self, x, y):
        pass

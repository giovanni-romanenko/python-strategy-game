
class Player:
    def __init__(self, name, color):
        self._name = name
        self._color = color
        self._cellCaptureCnt = 1

    def getName(self):
        return self._name

    def getColor(self):
        return self._color

    def choosesCharacterInteractivly(self) -> bool:
        pass

    def chooseChar(self, gameInfo, charToChooseFrom, playerNum):
        pass

    def makesTurnsInteractivly(self) -> bool:
        pass

    def takeCaptureDecision(self, gameInfo, gamePosition, playerNum):
        pass

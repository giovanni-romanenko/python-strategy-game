from .Player import Player


class LocalPlayer(Player):
    def __init__(self, name, color):
        super().__init__(name, color)

    def choosesCharacterInteractivly(self) -> bool:
        return True

    def chooseChar(self, gameInfo, charToChooseFrom, playerNum):
        return None

    def makesTurnsInteractivly(self) -> bool:
        return True

    def takeCaptureDecision(self, gameInfo, gamePosition, playerNum):
        return None

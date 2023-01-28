import random
from .Player import Player


class AIEasy(Player):
    def __init__(self, name, color):
        super().__init__(name, color)

    def choosesCharacterInteractivly(self) -> bool:
        return False

    def chooseChar(self, gameInfo, charToChooseFrom, playerNum):
        choiceSize = len(charToChooseFrom[playerNum])
        randomNum = random.randrange(0, choiceSize)
        return [charToChooseFrom[playerNum][randomNum], randomNum]

    def makesTurnsInteractivly(self) -> bool:
        return False

    def takeCaptureDecision(self, gameInfo, gamePosition, playerNum):
        allDecisions = gamePosition.generateAllValidGameInput()
        return random.sample(allDecisions, 1)[0]

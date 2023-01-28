from .chargenerators.CharGen import CharGen
from .chargenerators.CharGenRandList import CharGenRandList


class NonInteractiveCC:
    def __init__(self):
        self._charGenerator = CharGenRandList()

    def makeChoices(self, gameInfo):
        self._charGenerator.generateCharactersToChooseFrom(
            gameInfo.charChoiceList, gameInfo.characters)
        charToChooseFrom = self._charGenerator.getResult()
        self._chosenChars = list()
        curPlayer = 0
        while curPlayer < gameInfo.playerCnt:
            if gameInfo.players[curPlayer].choosesCharacterInteractivly():
                raise Exception(
                    "NonInteractiveCC class works only with non-interactive Players.")
            curChoice = gameInfo.players[curPlayer].chooseChar(
                gameInfo, charToChooseFrom, curPlayer)
            self._chosenChars.append(curChoice[0])
            curPlayer += 1
        gameInfo.chosenChars = self._chosenChars

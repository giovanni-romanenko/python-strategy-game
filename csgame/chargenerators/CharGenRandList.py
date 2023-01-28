import random
from .CharGen import CharGen


class CharGenRandList(CharGen):
    def __init__(self):
        super().__init__()

    def generateCharactersToChooseFrom(self, listOfAmountsOfChars, allCharacters) -> bool:
        """
           Generates listOfAmountsOfChars[i] different characters for i-th player from allCharacters.
           All chosen characters are different. This method does not return result. Result is
           got afterwards by method getResult().
        """
        totalCharCnt = sum(listOfAmountsOfChars)
        if totalCharCnt > len(allCharacters):
            return False
        chosenChars = random.sample(allCharacters, totalCharCnt)
        prevI = 0
        nextI = 0
        i = 0
        cnt = len(listOfAmountsOfChars)
        self._res.clear()
        while i < cnt:
            prevI = nextI
            nextI += listOfAmountsOfChars[i]
            self._res.append(chosenChars[prevI:nextI])
            i += 1
        return True

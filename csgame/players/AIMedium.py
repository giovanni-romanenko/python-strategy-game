import copy
import random
import numpy as np
from .Player import Player


class AIMedium(Player):
    _winProbabilityData = {
        "Cat": {
            "Clown-Wolf": 2 / 180,
            "Eternal Flame": 47 / 180,
            "Mirror": 46 / 180,
            "Rich Pig": 15 / 180,
            "Second Wife": 36 / 180,
            "Water Bucket": 44 / 180,
            "Yin": 10 / 180
        },
        "Clown-Wolf": {
            "Cat": 134 / 180,
            "Eternal Flame": 106 / 180,
            "Mirror": 50 / 180,
            "Rich Pig": 139 / 180,
            "Second Wife": 137 / 180,
            "Water Bucket": 140 / 180,
            "Yin": 105 / 180
        },
        "Eternal Flame": {
            "Cat": 63 / 180,
            "Clown-Wolf": 11 / 180,
            "Mirror": 53 / 180,
            "Rich Pig": 31 / 180,
            "Second Wife": 58 / 180,
            "Water Bucket": 41 / 180,
            "Yin": 23 / 180
        },
        "Mirror": {
            "Cat": 50 / 180,
            "Clown-Wolf": 41 / 180,
            "Eternal Flame": 44 / 180,
            "Rich Pig": 42 / 180,
            "Second Wife": 46 / 180,
            "Water Bucket": 53 / 180,
            "Yin": 51 / 180
        },
        "Rich Pig": {
            "Cat": 86 / 180,
            "Clown-Wolf": 2 / 180,
            "Eternal Flame": 62 / 180,
            "Mirror": 45 / 180,
            "Second Wife": 87 / 180,
            "Water Bucket": 78 / 180,
            "Yin": 47 / 180
        },
        "Second Wife": {
            "Cat": 57 / 180,
            "Clown-Wolf": 5 / 180,
            "Eternal Flame": 35 / 180,
            "Mirror": 42 / 180,
            "Rich Pig": 20 / 180,
            "Water Bucket": 57 / 180,
            "Yin": 6 / 180
        },
        "Water Bucket": {
            "Cat": 53 / 180,
            "Clown-Wolf": 1 / 180,
            "Eternal Flame": 57 / 180,
            "Mirror": 55 / 180,
            "Rich Pig": 18 / 180,
            "Second Wife": 41 / 180,
            "Yin": 10 / 180
        },
        "Yin": {
            "Cat": 106 / 180,
            "Clown-Wolf": 8 / 180,
            "Eternal Flame": 78 / 180,
            "Mirror": 42 / 180,
            "Rich Pig": 56 / 180,
            "Second Wife": 124 / 180,
            "Water Bucket": 98 / 180
        }
    }

    def __init__(self, name, color):
        super().__init__(name, color)

    def choosesCharacterInteractivly(self) -> bool:
        return False

    def chooseChar(self, gameInfo, charToChooseFrom, playerNum):
        if gameInfo.playerCnt != 2 or len(
                charToChooseFrom[0]) != 2 or len(charToChooseFrom[1]) != 2:
            raise Exception(
                "AIMedium character choice is written only for case of 2 players and 2 characters for each player.")
        if playerNum == 0:
            myCharacters = charToChooseFrom[0]
            opponentCharacters = charToChooseFrom[1]
        else:
            myCharacters = charToChooseFrom[1]
            opponentCharacters = charToChooseFrom[0]
        winProbFirstvsFirst = self._winProbabilityData[myCharacters[0].getName(
        )][opponentCharacters[0].getName()]
        winProbFirstvsSecond = self._winProbabilityData[myCharacters[0].getName(
        )][opponentCharacters[1].getName()]
        winProbSecondvsFirst = self._winProbabilityData[myCharacters[1].getName(
        )][opponentCharacters[0].getName()]
        winProbSecondvsSecond = self._winProbabilityData[myCharacters[1].getName(
        )][opponentCharacters[1].getName()]
        minWinProbOfFirst = min(winProbFirstvsFirst, winProbFirstvsSecond)
        minWinProbOfSecond = min(winProbSecondvsFirst, winProbSecondvsSecond)
        if minWinProbOfFirst > minWinProbOfSecond:
            myChoice = [myCharacters[0], 0]
        else:
            myChoice = [myCharacters[1], 1]
        return myChoice

    def makesTurnsInteractivly(self) -> bool:
        return False

    def takeCaptureDecision(self, gameInfo, gamePosition, playerNum):
        if gamePosition.phase == "Playing":
            return self._takeCaptureDecisionPlayingPhase(
                gameInfo, gamePosition, playerNum)
        elif gamePosition.phase == "Choosing start cells":
            return self._takeCaptureDecisionChoosingPhase(
                gameInfo, gamePosition, playerNum)
        return None

    def _takeCaptureDecisionChoosingPhase(
            self, gameInfo, gamePosition, playerNum):
        allDecisions = gamePosition.generateAllValidGameInput()
        return random.sample(allDecisions, 1)[0]

    def _evaluatePosition(self, gameInfo, gamePosition, playerNum):
        captureLeftCnt = gamePosition.curPlayerCellCaptureCnt
        if gamePosition.curPlayer != playerNum:
            captureLeftCnt = 0
        capturedCnt = np.count_nonzero(gamePosition.ownageData == playerNum)
        return capturedCnt + captureLeftCnt

    def _takeCaptureDecisionPlayingPhase(
            self, gameInfo, gamePosition, playerNum):
        """Takes greedy decision on max depth of 3. On each level we go through 10+2*leftDepth decisions deeper at most."""
        gamePositionsOnGivenDepth = list()
        self._takeCaptureDecisionPlayingPhaseRec(
            gameInfo, gamePosition, playerNum, 3, gamePositionsOnGivenDepth, list())
        finalDecisionList = list()
        finalDecisionEndValue = -1
        for resultPosition in gamePositionsOnGivenDepth:
            curResultValue = self._evaluatePosition(
                resultPosition[1], resultPosition[2], playerNum)
            if curResultValue > finalDecisionEndValue:
                finalDecisionList.clear()
                finalDecisionList.append(resultPosition[0][0])
                finalDecisionEndValue = curResultValue
            elif curResultValue == finalDecisionEndValue:
                finalDecisionList.append(resultPosition[0][0])
        return random.sample(finalDecisionList, 1)[0]

    def _takeCaptureDecisionPlayingPhaseRec(
            self, gameInfo, gamePosition, playerNum, leftDepth, result, curCaptureSeq):
        if gamePosition.curPlayer != playerNum or gamePosition.checkFinished() or leftDepth == 0:
            result.append([copy.copy(curCaptureSeq), gameInfo, gamePosition])
            return None
        allDecisions = gamePosition.generateAllValidGameInput()
        if len(allDecisions) > 10 + 2 * leftDepth:
            allDecisions = random.sample(allDecisions, 10 + 2 * leftDepth)
        for decision in allDecisions:
            curGameInfo = gameInfo.getCopy()
            curGamePosition = gamePosition.getDeepCopy(curGameInfo)
            curGamePosition.workWithInput(decision)
            curCaptureSeq.append(decision)
            self._takeCaptureDecisionPlayingPhaseRec(
                curGameInfo, curGamePosition, playerNum, leftDepth - 1, result, curCaptureSeq
            )
            curCaptureSeq.pop()

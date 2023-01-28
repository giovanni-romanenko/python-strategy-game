from .CCScreenButton import CCScreenButton
from .CCScreenDesc import CCScreenDesc


class CCScreenCB:
    def __init__(self, window, gameInfo, charToChooseFrom, batch):
        self._window = window
        self._gameInfo = gameInfo
        self._charToChooseFrom = charToChooseFrom
        self._mainPartWidth = self._window.width
        self._mainPartHeight = (9 * self._window.height) // 10
        self._charButtonsList = list()
        self._charDescList = list()
        self._charButtonsPlayerNum = list()
        self._playerNumToButton = list()
        self._buttonWidth = (
            2 * (self._mainPartWidth // (self._gameInfo.playerCnt + 1))) // 3
        curPlayer = 0
        curButtonNum = 0
        while curPlayer < self._gameInfo.playerCnt:
            curButton = 0
            totalButtons = len(charToChooseFrom[curPlayer])
            curPlayerNumToButtonList = list()
            while curButton < totalButtons:
                curSizes = min(
                    self._buttonWidth, (2 * (self._mainPartHeight // (totalButtons + 1))) // 3)
                self._charButtonsList.append(CCScreenButton(
                    (((curPlayer + 1) * self._mainPartWidth) //
                     (self._gameInfo.playerCnt + 1)) - curSizes // 2,
                    (((curButton + 1) * self._mainPartHeight) //
                     (totalButtons + 1)) - curSizes // 2,
                    curSizes, curSizes,
                    charToChooseFrom[curPlayer][curButton],
                    5, (255, 255, 255),
                    batch, 2
                ))
                self._charButtonsPlayerNum.append([curPlayer, curButton])
                curPlayerNumToButtonList.append(curButtonNum)
                descBorder = 5
                self._charDescList.append(CCScreenDesc(
                    (((curPlayer + 1) * self._mainPartWidth) //
                     (self._gameInfo.playerCnt + 1)) + (curSizes // 2) + (2 * descBorder),
                    ((curButton * self._mainPartHeight) //
                     (totalButtons + 1)) + curSizes // 6,
                    ((17 * self._mainPartWidth) //
                     (30 * (self._gameInfo.playerCnt + 1))) - (4 * descBorder),
                    (self._mainPartHeight // (totalButtons + 1)) + curSizes // 3,
                    charToChooseFrom[curPlayer][curButton], batch, 5,
                    (225, 225, 225), descBorder, (30, 30, 30), (0, 0, 0, 255)
                ))
                curButton += 1
                curButtonNum += 1
            self._playerNumToButton.append(curPlayerNumToButtonList)
            curPlayer += 1

    def onMousePressRoutine(self, x, y, button, modifiers, playerNum):
        if playerNum is None:
            return None
        if self._gameInfo.players[playerNum].choosesCharacterInteractivly():
            foundButton = self._checkMouseIsOverButton(x, y)
            if foundButton is not None and self._charButtonsPlayerNum[foundButton][0] == playerNum:
                return [self._charToChooseFrom[self._charButtonsPlayerNum[foundButton][0]][self._charButtonsPlayerNum[foundButton][1]],
                        self._charButtonsPlayerNum[foundButton][1]]
        return None

    def onMouseMotionRoutine(self, x, y, dx, dy):
        i = 0
        for charButton in self._charButtonsList:
            if charButton.checkMouseIsOver(x, y):
                self._charDescList[i].makeVisible()
            else:
                self._charDescList[i].makeInvisible()
            i += 1

    def chooseButton(self, playerNum, button):
        self._charButtonsList[self._playerNumToButton[playerNum][button]].changeBorderColor(
            self._gameInfo.players[playerNum].getColor()
        )

    def _checkMouseIsOverButton(self, x, y):
        curButton = 0
        buttonCnt = len(self._charButtonsList)
        while curButton < buttonCnt:
            if self._charButtonsList[curButton].checkMouseIsOver(x, y):
                return curButton
            curButton += 1
        return None

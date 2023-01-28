import words
from .CellType import CellType


class DarkCell(CellType):
    def __init__(self, imageFile=None):
        super().__init__(imageFile)
        self._name = "Dark"
        self._color = (30, 30, 30)

    def isWatery(self):
        return False

    def checkBasicCaptureIsPossible(
            self, gamePosition, fromCell, toCell, capture_points_check=True):
        curChar = gamePosition.gameInfo.chosenChars[gamePosition.curPlayer]
        if (capture_points_check and gamePosition.curPlayerCellCaptureCnt <
                1) or curChar.isHoly():
            return False
        return True

    def onCaptureTo(self, gamePosition, captureData):
        return None

    def onCaptureToPhaseTwo(self, gamePosition, captureData):
        return None

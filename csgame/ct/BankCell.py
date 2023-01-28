import words
from .CellType import CellType


class BankCell(CellType):
    def __init__(self, imageFile=None):
        super().__init__(imageFile)
        self._name = "Bank"
        self._color = (255, 215, 0)

    def isWatery(self):
        return False

    def checkBasicCaptureIsPossible(
            self, gamePosition, fromCell, toCell, capture_points_check=True):
        if (not capture_points_check or gamePosition.curPlayerCellCaptureCnt >= 1):
            return True
        return False

    def onCaptureTo(self, gamePosition, captureData):
        return None

    def onCaptureToPhaseTwo(self, gamePosition, captureData):
        oldBankCnt = gamePosition.cntCellsOfGivenCellType("Bank")
        if oldBankCnt % 2 == 1:
            gamePosition.curPlayerCellCaptureCnt += 1

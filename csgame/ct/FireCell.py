import words
from .CellType import CellType


class FireCell(CellType):
    def __init__(self, imageFile=None):
        super().__init__(imageFile)
        self._name = "Fire"
        self._color = (242, 125, 12)

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
        return None

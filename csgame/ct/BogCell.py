import words
from .CellType import CellType


class BogCell(CellType):
    def __init__(self, imageFile=None):
        super().__init__(imageFile)
        self._name = "Bog"
        self._color = (0, 100, 0)

    def isWatery(self):
        return True

    def checkBasicCaptureIsPossible(
            self, gamePosition, fromCell, toCell, capture_points_check=True):
        if (not capture_points_check or gamePosition.curPlayerCellCaptureCnt >= 1):
            return True
        return False

    def onCaptureTo(self, gamePosition, captureData):
        return None

    def onCaptureToPhaseTwo(self, gamePosition, captureData):
        return None

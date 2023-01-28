import words
from .CellType import CellType


class PigsCell(CellType):
    def __init__(self, imageFile=None):
        super().__init__(imageFile)
        self._name = "Pigs"
        self._color = (255, 20, 147)

    def isWatery(self):
        return False

    def checkBasicCaptureIsPossible(
            self, gamePosition, fromCell, toCell, capture_points_check=True):
        if (not capture_points_check or gamePosition.curPlayerCellCaptureCnt >= 0):
            return True
        return False

    def onCaptureTo(self, gamePosition, captureData):
        gamePosition.curPlayerCellCaptureCnt += 1

    def onCaptureToPhaseTwo(self, gamePosition, captureData):
        return None

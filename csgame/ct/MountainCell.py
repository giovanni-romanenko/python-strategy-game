import words
from .CellType import CellType


class MountainCell(CellType):
    def __init__(self, imageFile=None):
        super().__init__(imageFile)
        self._name = "Mountain"
        self._color = (101, 67, 33)

    def isWatery(self):
        return False

    def checkBasicCaptureIsPossible(
            self, gamePosition, fromCell, toCell, capture_points_check=True):
        return False

    def onCaptureTo(self, gamePosition, captureData):
        return None

    def onCaptureToPhaseTwo(self, gamePosition, captureData):
        return None

import words
from .CellType import CellType


class IceCell(CellType):
    def __init__(self, imageFile=None):
        super().__init__(imageFile)
        self._name = "Ice"
        self._color = (0, 200, 200)

    def isWatery(self):
        return True

    def checkBasicCaptureIsPossible(
            self, gamePosition, fromCell, toCell, capture_points_check=True):
        if (not capture_points_check or gamePosition.curPlayerCellCaptureCnt >= 1):
            return True
        return False

    def onCaptureTo(self, gamePosition, captureData):
        fieldCellTypesNums = gamePosition.field.getFieldCellTypesNums()
        fireCTNum = gamePosition.gameInfo.cellTypeNumByName["Fire"]
        if fieldCellTypesNums[captureData[0][0]
                              ][captureData[0][1]] == fireCTNum:
            waterCTNum = gamePosition.gameInfo.cellTypeNumByName["Water"]
            fieldCellTypesNums[captureData[1][0]
                               ][captureData[1][1]] = waterCTNum

    def onCaptureToPhaseTwo(self, gamePosition, captureData):
        return None

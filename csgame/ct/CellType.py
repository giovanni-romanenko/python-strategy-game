import pyglet


class CellType:
    def __init__(self, imageFile=None):
        self._name = None
        self._color = None
        if imageFile is not None:
            self._image = pyglet.resource.image(imageFile)
        else:
            self._image = None

    def getName(self):
        return self._name

    def getColor(self):
        return self._color

    def getImage(self):
        return self._image

    def isWatery(self):
        pass

    def checkBasicCaptureIsPossible(
            self, gamePosition, fromCell, toCell, capture_points_check=True):
        pass

    def onCaptureTo(self, gamePosition, captureData):
        pass

    def onCaptureToPhaseTwo(self, gamePosition, captureData):
        pass

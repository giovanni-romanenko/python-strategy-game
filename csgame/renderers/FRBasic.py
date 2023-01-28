import pyglet
from .FieldRenderer import FieldRenderer


class FRBasic(FieldRenderer):
    def __init__(self, x, y, width, height, gameInfo, gamePosition, batch, groupNum, circleBorder, circleBorderColor,
                 lineColor, lineWidth, noOwnerColor, chosenCellColor):
        super().__init__(x, y, width, height, gameInfo, gamePosition, batch, groupNum)
        self._fieldWidth = self._gamePosition.field.getWidth()
        self._fieldHeight = self._gamePosition.field.getHeight()
        self._fieldCellTypes = self._gamePosition.field.getFieldCellTypesNums()
        self._noOwnerColor = noOwnerColor
        self._chosenCellColor = chosenCellColor
        self._typeRectangles = list()
        self._ownerCircleBorder = list()
        self._ownerCircle = list()
        curColNum = 0
        while curColNum < self._fieldWidth:
            curRowNum = 0
            curColTypeRectangles = list()
            curColOwnerCircleBorders = list()
            curColOwnerCircles = list()
            while curRowNum < self._fieldHeight:
                curColTypeRectangles.append(pyglet.shapes.Rectangle(
                    self._x + (curColNum * self._width) // self._fieldWidth, self._y +
                    (curRowNum * self._height) // self._fieldHeight,
                    self._width // self._fieldWidth, self._height // self._fieldHeight,
                    color=self._gameInfo.cellTypes[self._fieldCellTypes[curColNum][curRowNum]].getColor(
                    ),
                    batch=batch, group=pyglet.graphics.OrderedGroup(groupNum)
                ))
                curColTypeRectangles[curRowNum].opacity = 0
                curColOwnerCircleBorders.append(pyglet.shapes.Circle(
                    self._x + (((2 * curColNum + 1) * self._width) //
                               (2 * self._fieldWidth)),
                    self._y + (((2 * curRowNum + 1) * self._height) //
                               (2 * self._fieldHeight)),
                    (self._height // (4 * self._fieldHeight)) + circleBorder,
                    color=circleBorderColor, batch=batch,
                    group=pyglet.graphics.OrderedGroup(groupNum + 1)
                ))
                curColOwnerCircleBorders[curRowNum].opacity = 0
                ownerColor = noOwnerColor
                if self._gamePosition.ownageData[curColNum][curRowNum] != -1:
                    curOwner = self._gamePosition.ownageData[curColNum][curRowNum]
                    ownerColor = self._gameInfo.players[curOwner].getColor()
                curColOwnerCircles.append(pyglet.shapes.Circle(
                    self._x + (((2 * curColNum + 1) * self._width) //
                               (2 * self._fieldWidth)),
                    self._y + (((2 * curRowNum + 1) * self._height) //
                               (2 * self._fieldHeight)),
                    self._height // (4 * self._fieldHeight),
                    color=ownerColor, batch=batch,
                    group=pyglet.graphics.OrderedGroup(groupNum + 2)
                ))
                curColOwnerCircles[curRowNum].opacity = 0
                curRowNum += 1
            self._typeRectangles.append(curColTypeRectangles)
            self._ownerCircleBorder.append(curColOwnerCircleBorders)
            self._ownerCircle.append(curColOwnerCircles)
            curColNum += 1
        self._vertLines = list()
        curVertLine = 1
        while curVertLine < self._fieldWidth:
            self._vertLines.append(pyglet.shapes.Line(
                self._x + (curVertLine *
                           self._width) // self._fieldWidth, self._y,
                self._x +
                (curVertLine * self._width) // self._fieldWidth, self._y + self._height,
                width=lineWidth, color=lineColor, batch=batch, group=pyglet.graphics.OrderedGroup(
                    groupNum + 3)
            ))
            self._vertLines[curVertLine - 1].opacity = 0
            curVertLine += 1
        self._horLines = list()
        curHorLine = 1
        while curHorLine < self._fieldHeight:
            self._horLines.append(pyglet.shapes.Line(
                self._x, self._y +
                (curHorLine * self._height) // self._fieldHeight,
                self._x + self._width, self._y +
                (curHorLine * self._height) // self._fieldHeight,
                width=lineWidth, color=lineColor, batch=batch, group=pyglet.graphics.OrderedGroup(
                    groupNum + 3)
            ))
            self._horLines[curHorLine - 1].opacity = 0
            curHorLine += 1
        self.onChangeRoutine()

    def turnOn(self):
        for rectCol in self._typeRectangles:
            for rect in rectCol:
                rect.opacity = 255
        for ownCirBorCol in self._ownerCircleBorder:
            for ownCirBor in ownCirBorCol:
                ownCirBor.opacity = 255
        for ownCirCol in self._ownerCircle:
            for ownCir in ownCirCol:
                ownCir.opacity = 255
        for vertLine in self._vertLines:
            vertLine.opacity = 255
        for horLine in self._horLines:
            horLine.opacity = 255

    def turnOff(self):
        for rectCol in self._typeRectangles:
            for rect in rectCol:
                rect.opacity = 0
        for ownCirBorCol in self._ownerCircleBorder:
            for ownCirBor in ownCirBorCol:
                ownCirBor.opacity = 0
        for ownCirCol in self._ownerCircle:
            for ownCir in ownCirCol:
                ownCir.opacity = 0
        for vertLine in self._vertLines:
            vertLine.opacity = 0
        for horLine in self._horLines:
            horLine.opacity = 0

    def onChangeRoutine(self):
        if self._gamePosition.phase == "Playing":
            self._onChangeRoutinePlayingPhase()
        elif self._gamePosition.phase == "Choosing start cells":
            self._onChangeRoutineChoosingPhase()

    def _onChangeRoutinePlayingPhase(self):
        curColNum = 0
        while curColNum < self._fieldWidth:
            curRowNum = 0
            while curRowNum < self._fieldHeight:
                cellTypeColor = self._gameInfo.cellTypes[self._fieldCellTypes[curColNum][curRowNum]].getColor(
                )
                if self._typeRectangles[curColNum][curRowNum].color != cellTypeColor:
                    self._typeRectangles[curColNum][curRowNum].color = cellTypeColor
                ownerColor = self._noOwnerColor
                if self._gamePosition.ownageData[curColNum][curRowNum] != -1:
                    curOwner = self._gamePosition.ownageData[curColNum][curRowNum]
                    ownerColor = self._gameInfo.players[curOwner].getColor()
                if self._ownerCircle[curColNum][curRowNum].color != ownerColor:
                    self._ownerCircle[curColNum][curRowNum].color = ownerColor
                curRowNum += 1
            curColNum += 1
        curChosenCell = self._gamePosition.currentFromCell
        if curChosenCell is not None:
            if self._ownerCircle[curChosenCell[0]
                                 ][curChosenCell[1]].color != self._chosenCellColor:
                self._ownerCircle[curChosenCell[0]
                                  ][curChosenCell[1]].color = self._chosenCellColor

    def _onChangeRoutineChoosingPhase(self):
        curColNum = 0
        while curColNum < self._fieldWidth:
            curRowNum = 0
            while curRowNum < self._fieldHeight:
                cellTypeColor = self._gameInfo.cellTypes[self._fieldCellTypes[curColNum][curRowNum]].getColor(
                )
                if self._typeRectangles[curColNum][curRowNum].color != cellTypeColor:
                    self._typeRectangles[curColNum][curRowNum].color = cellTypeColor
                ownerColor = self._noOwnerColor
                if self._ownerCircle[curColNum][curRowNum].color != ownerColor:
                    self._ownerCircle[curColNum][curRowNum].color = ownerColor
                curRowNum += 1
            curColNum += 1
        curPlayer = 0
        while curPlayer < self._gameInfo.playerCnt:
            ownerColor = self._gameInfo.players[curPlayer].getColor()
            if self._gamePosition.chosenStartCells[curPlayer] is None:
                curStartCells = self._gamePosition.startCells[curPlayer]
                for startCell in curStartCells:
                    self._ownerCircle[startCell[0]
                                      ][startCell[1]].color = ownerColor
            else:
                chosenCell = self._gamePosition.chosenStartCells[curPlayer]
                self._ownerCircle[chosenCell[0]
                                  ][chosenCell[1]].color = ownerColor
            curPlayer += 1

    def findCellCoord(self, x, y):
        if x < self._x or x >= self._x + \
                self._width or y < self._y or y >= self._y + self._height:
            return None
        return [(self._fieldWidth * (x - self._x)) // self._width,
                (self._fieldHeight * (y - self._y)) // self._height]

import os
import pyglet

dirName = os.path.dirname(os.path.abspath(__file__))
pyglet.resource.path = [
    os.path.join(dirName, 'resource/media'),
    os.path.join(dirName, 'resource/png'),
    os.path.join(dirName, 'resource/language')
]

_languageFileList = ['English.txt', 'Text.txt']
_languageCnt = len(_languageFileList)
_languageIt = 0


class GameStringData:
    def __init__(self, fileName):
        self._fileName = fileName
        self._readDataFromFile(pyglet.resource.file(fileName, 'rt'))

    def changeLanguage(self, fileName):
        if self._fileName != fileName:
            self._fileName = fileName
            self._readDataFromFile(pyglet.resource.file(fileName, 'rt'))

    def _readDataFromFile(self, file):
        if file is None:
            raise Exception("Basic translation fiel does not exist.")
        lines = file.readlines()
        file.close()
        if len(lines) < 29:
            raise Exception("Basic translation file has wrong format.")
        self._newGame = lines[0].strip()
        self._settings = lines[1].strip()
        self._credits = lines[2].strip()
        self._exit = lines[3].strip()
        self._language = lines[4].strip()
        self._currentLanguage = lines[5].strip()
        self._fullscreen = lines[6].strip()
        self._on = lines[7].strip()
        self._off = lines[8].strip()
        self._musicVolume = lines[9].strip()
        self._createdBy = lines[10].strip()
        self._musicBy = lines[11].strip()
        self._time = lines[12].strip()
        self._holy = lines[13].strip()
        self._unholy = lines[14].strip()
        self._watery = lines[15].strip()
        self._nonWatery = lines[16].strip()
        self._totalCaptured = lines[17].strip()
        self._capturePnts = lines[18].strip()
        self._combo = lines[19].strip()
        self._victoryMessage = lines[20].strip()
        self._tieMessage = lines[21].strip()
        self._lossMessage = lines[22].strip()
        self._choosePlayer = lines[23].strip()
        self._localPlayer = lines[24].strip()
        self._easyAI = lines[25].strip()
        self._mediumAI = lines[26].strip()
        self._charFile = lines[27].strip()
        self._cellTypesFile = lines[28].strip()
        self._charNameData = dict()
        self._charDescData = dict()
        self._charRulesData = dict()
        if not self._readCharactersFromFile(self._charFile):
            raise Exception(
                "File with characters translation has wrong format.")
        self._ctNameData = dict()
        self._ctDescData = dict()
        if not self._readCellTypesFromFile(self._cellTypesFile):
            raise Exception(
                "File with cell types translation has wrong format.")

    def _readCharactersFromFile(self, fileName):
        file = pyglet.resource.file(fileName, 'rt')
        if file is None:
            raise Exception("File with characters translation does not exist.")
        lines = file.readlines()
        file.close()
        lineCnt = len(lines)
        curLineNum = 0
        while curLineNum < lineCnt:
            while curLineNum < lineCnt and lines[curLineNum].strip() == '':
                curLineNum += 1
            if curLineNum == lineCnt:
                return True
            curName = lines[curLineNum].strip()
            self._charDescData[curName] = list()
            self._charRulesData[curName] = ""
            curLineNum += 1
            if curLineNum == lineCnt:
                return False
            while lines[curLineNum].strip() == '':
                curLineNum += 1
                if curLineNum == lineCnt:
                    return False
            if lines[curLineNum].strip() != 'TRANSLATED':
                return False
            curLineNum += 1
            if curLineNum == lineCnt:
                return False
            self._charNameData[curName] = lines[curLineNum].strip()
            curLineNum += 1
            if curLineNum == lineCnt:
                return False
            while lines[curLineNum].strip() == '':
                curLineNum += 1
                if curLineNum == lineCnt:
                    return False
            if lines[curLineNum].strip() != 'DESCRIPTION':
                return False
            curLineNum += 1
            if curLineNum == lineCnt:
                return False
            while lines[curLineNum].strip() != 'RULES':
                self._charDescData[curName].append(lines[curLineNum].strip())
                curLineNum += 1
                if curLineNum == lineCnt:
                    return False
            curLineNum += 1
            if curLineNum == lineCnt:
                return False
            while lines[curLineNum].strip() != 'END':
                self._charRulesData[curName] += lines[curLineNum]
                curLineNum += 1
                if curLineNum == lineCnt:
                    return False
            curLineNum += 1
        return True

    def _readCellTypesFromFile(self, fileName):
        file = pyglet.resource.file(fileName, 'rt')
        if file is None:
            raise Exception(
                "File with cell types translation does not exists.")
        lines = file.readlines()
        file.close()
        lineCnt = len(lines)
        curLineNum = 0
        while curLineNum < lineCnt:
            while curLineNum < lineCnt and lines[curLineNum].strip() == '':
                curLineNum += 1
            if curLineNum == lineCnt:
                return True
            curName = lines[curLineNum].strip()
            self._ctNameData
            curLineNum += 1
            if curLineNum == lineCnt:
                return False
            while lines[curLineNum].strip() == '':
                curLineNum += 1
                if curLineNum == lineCnt:
                    return False
            if lines[curLineNum].strip() != 'TRANSLATED':
                return False
            curLineNum += 1
            if curLineNum == lineCnt:
                return False
            self._ctNameData[curName] = lines[curLineNum].strip()
            curLineNum += 1
            if curLineNum == lineCnt:
                return False
            while lines[curLineNum].strip() == '':
                curLineNum += 1
                if curLineNum == lineCnt:
                    return False
            if lines[curLineNum].strip() != 'DESCRIPTION':
                return False
            curLineNum += 1
            if curLineNum == lineCnt:
                return False
            self._ctDescData[curName] = lines[curLineNum].strip()
            curLineNum += 1
            if curLineNum == lineCnt:
                return False
            while lines[curLineNum].strip() == '':
                curLineNum += 1
                if curLineNum == lineCnt:
                    return False
            if lines[curLineNum].strip() != 'END':
                return False
            curLineNum += 1
        return True

    def characterName(self, name):
        return self._charNameData[name]

    def characterDescription(self, name):
        return self._charDescData[name]

    def characterRulesDescription(self, name):
        return self._charRulesData[name]

    def cellTypeName(self, name):
        return self._ctNameData[name]

    def cellTypeDescription(self, name):
        return self._ctDescData[name]

    def newGame(self):
        return self._newGame

    def settings(self):
        return self._settings

    def credits(self):
        return self._credits

    def exit(self):
        return self._exit

    def language(self):
        return self._language

    def currentLanguage(self):
        return self._currentLanguage

    def fullscreen(self):
        return self._fullscreen

    def on(self):
        return self._on

    def off(self):
        return self._off

    def musicVolume(self):
        return self._musicVolume

    def createdBy(self):
        return self._createdBy

    def musicBy(self):
        return self._musicBy

    def time(self):
        return self._time

    def holy(self):
        return self._holy

    def unholy(self):
        return self._unholy

    def watery(self):
        return self._watery

    def nonWatery(self):
        return self._nonWatery

    def totalCaptured(self):
        return self._totalCaptured

    def capturePnts(self):
        return self._capturePnts

    def combo(self):
        return self._combo

    def victoryMessage(self):
        return self._victoryMessage

    def tieMessage(self):
        return self._tieMessage

    def lossMessage(self):
        return self._lossMessage

    def chooseSecondPlayer(self):
        return self._choosePlayer

    def localPlayer(self):
        return self._localPlayer

    def easyAI(self):
        return self._easyAI

    def mediumAI(self):
        return self._mediumAI


word = GameStringData(_languageFileList[_languageIt])


def setNextLanguage():
    global _languageFileList
    global _languageCnt
    global _languageIt
    _languageIt += 1
    if _languageIt == _languageCnt:
        _languageIt = 0
    word.changeLanguage(_languageFileList[_languageIt])

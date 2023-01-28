import pyglet
import words
from .MenuButton import MenuButton
from .GInitScreen import GInitScreen
from .GameInfo import GameInfo
from .players.Player import Player
from .players.LocalPlayer import LocalPlayer
from .players.AIEasy import AIEasy
from .players.AIMedium import AIMedium
from .characters.Character import Character
from .characters.AdmiralTriangle import AdmiralTriangle
from .characters.Cat import Cat
from .characters.ClownWolf import ClownWolf
from .characters.EternalFlame import EternalFlame
from .characters.Mirror import Mirror
from .characters.RichPig import RichPig
from .characters.SecondWife import SecondWife
from .characters.WaterBucket import WaterBucket
from .characters.Yin import Yin
from .ct.CellType import CellType
from .ct.BankCell import BankCell
from .ct.BloodCell import BloodCell
from .ct.BogCell import BogCell
from .ct.DarkCell import DarkCell
from .ct.FireCell import FireCell
from .ct.ForestCell import ForestCell
from .ct.IceCell import IceCell
from .ct.MountainCell import MountainCell
from .ct.PigsCell import PigsCell
from .ct.WaterCell import WaterCell


class GameSetupScreen:
    def __init__(self, window, parent, player, endWindow):
        self._window = window
        self._parent = parent
        self._mediaPlayer = player
        self._endWindow = endWindow
        self._screenBatch = pyglet.graphics.Batch()
        self._gameInitScreen = GInitScreen(window, self._endWindow)

    def screenInit(self):
        self._window.push_handlers(
            on_key_press=self._onKeyPress,
            on_mouse_press=self._onMousePress,
            on_draw=self._onDraw)
        self._playerList = [LocalPlayer('The Player', (0, 210, 0)), None]
        self._secondPlayerChoiceButtons = [
            MenuButton(
                self._window.width // 4, (3 * self._window.height) // 4,
                self._window.width // 2, self._window.height // 6,
                words.word.chooseSecondPlayer(), self._screenBatch
            ),
            MenuButton(
                self._window.width // 3, (self._window.height) // 2,
                self._window.width // 3, self._window.height // 6,
                words.word.localPlayer(), self._screenBatch
            ),
            MenuButton(
                self._window.width // 3, (self._window.height) // 3,
                self._window.width // 3, self._window.height // 6,
                words.word.easyAI(), self._screenBatch
            ),
            MenuButton(
                self._window.width // 3, (self._window.height) // 6,
                self._window.width // 3, self._window.height // 6,
                words.word.mediumAI(), self._screenBatch
            )
        ]
        self._reactions = [
            self._dummy,
            self._localPlayerChoice,
            self._easyAIChoice,
            self._mediumAIChoice]

    def _screenEnd(self):
        self._window.pop_handlers()
        for button in self._secondPlayerChoiceButtons:
            button.changeBatch(None)
        self._parent.screenInit()

    def _dummy(self):
        return None

    def _localPlayerChoice(self):
        self._playerList[1] = LocalPlayer('Opponent', (210, 0, 0))
        self._gameStart()

    def _easyAIChoice(self):
        self._playerList[1] = AIEasy('Opponent', (210, 0, 0))
        self._gameStart()

    def _mediumAIChoice(self):
        self._playerList[1] = AIMedium('Opponent', (210, 0, 0))
        self._gameStart()

    def _gameStart(self):
        self._gameInfo = GameInfo(self._playerList, 0,
                                  [Cat('Cat.png'), ClownWolf('ClownWolf.png'), EternalFlame('EternalFlame.png'),
                                   Mirror('Mirror.png'), RichPig(
                                       'RichPig.png'), SecondWife('SecondWife.png'),
                                   WaterBucket('WaterBucket.png'), Yin('Yin.png')],
                                  [2, 2], 2, [[8, 6], [8, 6]],
                                  [[0, 1], [1, 0]], [[2, 0], [2, 0]],
                                  [BankCell('Bank.png'), BloodCell('Blood.png'), BogCell('Bog.png'),
                                   DarkCell('Dark.png'), FireCell(
                                       'Fire.png'), ForestCell('Forest.png'),
                                   IceCell('Ice.png'), MountainCell(
                                       'Mountain.png'), PigsCell('Pigs.png'),
                                   WaterCell('Water.png')],
                                  [[2, 2], [2, 2]])
        self._window.pop_handlers()
        for button in self._secondPlayerChoiceButtons:
            button.changeBatch(None)
        self._mediaPlayer.pause()
        self._gameInitScreen.screenInit(
            self._gameInfo, self._mediaPlayer.volume)

    def _onKeyPress(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self._screenEnd()
        return True

    def _onMousePress(self, x, y, button, modifiers):
        i = 0
        for button in self._secondPlayerChoiceButtons:
            if button.checkCursorOnButton(x, y):
                self._reactions[i]()
            i += 1
        return True

    def _onDraw(self):
        self._window.clear()
        self._screenBatch.draw()
        return True

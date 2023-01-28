from csgame.players.Player import Player
from csgame.players.AIEasy import AIEasy
from csgame.players.AIMedium import AIMedium
from csgame.characters.Character import Character
from csgame.characters.Cat import Cat
from csgame.characters.ClownWolf import ClownWolf
from csgame.characters.EternalFlame import EternalFlame
from csgame.characters.Mirror import Mirror
from csgame.characters.RichPig import RichPig
from csgame.characters.SecondWife import SecondWife
from csgame.characters.WaterBucket import WaterBucket
from csgame.characters.Yin import Yin
from csgame.ct.CellType import CellType
from csgame.ct.BankCell import BankCell
from csgame.ct.BloodCell import BloodCell
from csgame.ct.BogCell import BogCell
from csgame.ct.DarkCell import DarkCell
from csgame.ct.FireCell import FireCell
from csgame.ct.ForestCell import ForestCell
from csgame.ct.IceCell import IceCell
from csgame.ct.MountainCell import MountainCell
from csgame.ct.PigsCell import PigsCell
from csgame.ct.WaterCell import WaterCell
from csgame.GameInfo import GameInfo
from csgame.NonInteractiveGame import NonInteractiveGame


def charByNum(number):
    if number == 0:
        return Cat()
    elif number == 1:
        return ClownWolf()
    elif number == 2:
        return EternalFlame()
    elif number == 3:
        return Mirror()
    elif number == 4:
        return RichPig()
    elif number == 5:
        return SecondWife()
    elif number == 6:
        return WaterBucket()
    elif number == 7:
        return Yin()


def playGamesWithGivenCharacters(firstChar, secondChar, gameCnt):
    charList = [charByNum(firstChar), charByNum(secondChar)]
    stats = [0, 0, 0]  # won by first, tied, won by second
    gameNum = 0
    while gameNum < gameCnt:
        curGame = NonInteractiveGame(GameInfo(
            [AIMedium('The Player', (0, 210, 0)), AIMedium('Opponent', (210, 0, 0))], 0,
            [Cat(), ClownWolf(), EternalFlame(), Mirror(), RichPig(), SecondWife(), WaterBucket(), Yin()],
            [2, 2], 2, [[8, 6], [8, 6]], [[0, 1], [1, 0]], [[2, 0], [2, 0]], [
                BankCell(), BloodCell(), BogCell(), DarkCell(), FireCell(), ForestCell(), IceCell(),
                MountainCell(), PigsCell(), WaterCell()
            ], [[2, 2], [2, 2]]
        ), charList)
        gameResult = curGame.play()
        if gameResult[0] > gameResult[1]:
            stats[0] += 1
        elif gameResult[0] < gameResult[1]:
            stats[2] += 1
        elif gameResult[0] == gameResult[1]:
            stats[1] += 1
        gameNum += 1
    print(
        charByNum(firstChar).getName() +
        " vs. " +
        charByNum(secondChar).getName())
    print(charByNum(firstChar).getName() + " won: " + str(stats[0]))
    print(charByNum(secondChar).getName() + " won: " + str(stats[2]))
    print("Tied: " + str(stats[1]))
    print()


firstChar = 0
while firstChar < 8:
    secondChar = firstChar + 1
    while secondChar < 8:
        playGamesWithGivenCharacters(firstChar, secondChar, 30)
        secondChar += 1
    firstChar += 1

import pytest
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
from csgame.NonInteractiveCC import NonInteractiveCC


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


def playGamesWithGivenCharacters(
        firstChar,
        secondChar,
        firstaitype,
        secondaitype,
        gameCnt):
    charList = [charByNum(firstChar), charByNum(secondChar)]
    playerList = [None, None]
    if firstaitype == "easy":
        playerList[0] = AIEasy('The Player', (0, 210, 0))
    else:
        playerList[0] = AIMedium('The Player', (0, 210, 0))
    if secondaitype == "easy":
        playerList[1] = AIEasy('Opponent', (210, 0, 0))
    else:
        playerList[1] = AIMedium('Opponent', (210, 0, 0))
    gameNum = 0
    while gameNum < gameCnt:
        curGame = NonInteractiveGame(GameInfo(
            playerList, 0,
            [Cat(), ClownWolf(), EternalFlame(), Mirror(), RichPig(), SecondWife(), WaterBucket(), Yin()],
            [2, 2], 2, [[8, 6], [8, 6]], [[0, 1], [1, 0]], [[2, 0], [2, 0]], [
                BankCell(), BloodCell(), BogCell(), DarkCell(), FireCell(), ForestCell(), IceCell(),
                MountainCell(), PigsCell(), WaterCell()
            ], [[2, 2], [2, 2]]
        ), charList)
        gameResult = curGame.play()
        if sum(gameResult) != 4:
            return False
        gameNum += 1
    return True


def playGamesWithCharChoice(firstaitype, secondaitype):
    playerList = [None, None]
    if firstaitype == "easy":
        playerList[0] = AIEasy('The Player', (0, 210, 0))
    else:
        playerList[0] = AIMedium('The Player', (0, 210, 0))
    if secondaitype == "easy":
        playerList[1] = AIEasy('Opponent', (210, 0, 0))
    else:
        playerList[1] = AIMedium('Opponent', (210, 0, 0))
    gameInfo = GameInfo(
        playerList, 0,
        [Cat(), ClownWolf(), EternalFlame(), Mirror(), RichPig(), SecondWife(), WaterBucket(), Yin()],
        [2, 2], 2, [[8, 6], [8, 6]], [[0, 1], [1, 0]], [[2, 0], [2, 0]], [
            BankCell(), BloodCell(), BogCell(), DarkCell(), FireCell(), ForestCell(), IceCell(),
            MountainCell(), PigsCell(), WaterCell()
        ], [[2, 2], [2, 2]]
    )
    nonInterCC = NonInteractiveCC()
    nonInterCC.makeChoices(gameInfo)
    curGame = NonInteractiveGame(gameInfo, gameInfo.chosenChars)
    gameResult = curGame.play()
    if sum(gameResult) != 4:
        return False
    return True


def playGamesWithCharChoiceMultipleTimes(firstaitype, secondaitype, gameCnt):
    curGame = 0
    while curGame < gameCnt:
        if not playGamesWithCharChoice(firstaitype, secondaitype):
            return False
        curGame += 1
    return True


def test_AIEasy_vs_AIEasy_each_character_pair_many_times():
    firstChar = 0
    while firstChar < 8:
        secondChar = firstChar + 1
        while secondChar < 8:
            assert(
                playGamesWithGivenCharacters(
                    firstChar,
                    secondChar,
                    "easy",
                    "easy",
                    10))
            secondChar += 1
        firstChar += 1


def test_AIEasy_vs_AIMedium_each_character_pair():
    firstChar = 0
    while firstChar < 8:
        secondChar = 0
        while secondChar < 8:
            if secondChar != firstChar:
                assert(
                    playGamesWithGivenCharacters(
                        firstChar,
                        secondChar,
                        "easy",
                        "medium",
                        1))
            secondChar += 1
        firstChar += 1


def test_AIMedium_vs_AIMedium_each_character_pair():
    firstChar = 0
    while firstChar < 8:
        secondChar = firstChar + 1
        while secondChar < 8:
            assert(
                playGamesWithGivenCharacters(
                    firstChar,
                    secondChar,
                    "medium",
                    "medium",
                    1))
            secondChar += 1
        firstChar += 1


def test_AIEasy_vs_AIEasy_with_character_choice_many_times():
    assert(playGamesWithCharChoiceMultipleTimes("easy", "easy", 100))


def test_AIEasy_vs_AIMedium_with_character_choice_many_times():
    assert(playGamesWithCharChoiceMultipleTimes("easy", "medium", 20))


def test_AIMedium_vs_AIMedium_with_character_choice_many_times():
    assert(playGamesWithCharChoiceMultipleTimes("medium", "medium", 10))

import pyglet
import random


class GameMediaPlayer:
    def __init__(self, gameMediaPlayer, gameMusicList):
        self._gameMediaPlayer = gameMediaPlayer
        self._gameMusicList = gameMusicList
        self._gameMusicSources = []
        for sourceName in gameMusicList:
            self._gameMusicSources.append(pyglet.resource.media(sourceName))

    def play(self):
        self._gameMediaPlayer.play()

    def pause(self):
        self._gameMediaPlayer.pause()

    def checkPlayingSource(self):
        if self._gameMediaPlayer.source is None:
            random.shuffle(self._gameMusicSources)
            for source in self._gameMusicSources:
                self._gameMediaPlayer.queue(source)
            self._gameMediaPlayer.play()

    def isPlaying(self):
        return self._gameMediaPlayer.playing

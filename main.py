import pyglet
import os
from csgame.MainMenu import MainMenu

dirName = os.path.dirname(os.path.abspath(__file__))
pyglet.resource.path = [
    os.path.join(dirName, 'resource/media'),
    os.path.join(dirName, 'resource/png'),
    os.path.join(dirName, 'resource/language')
]

window = pyglet.window.Window(width=1024, height=576)
mm = MainMenu(window)
mm.screenInit()
pyglet.app.run()

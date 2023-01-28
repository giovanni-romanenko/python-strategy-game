import pyglet
from .MenuButton import MenuButton


class GamePause:
    def __init__(self, window, parent):
        self._window = window
        self._parent = parent
        self._pauseLabelInfo = [1, 3, 3, 4, 1, 3, 1, 4, 'PAUSE']
        self._pauseLabel = MenuButton(self._pauseLabelInfo[0] * self._window.width // self._pauseLabelInfo[1],
                                      self._pauseLabelInfo[2] *
                                      self._window.height // self._pauseLabelInfo[3],
                                      self._pauseLabelInfo[4] *
                                      self._window.width // self._pauseLabelInfo[5],
                                      self._pauseLabelInfo[6] *
                                      self._window.height // self._pauseLabelInfo[7],
                                      self._pauseLabelInfo[8])

    def setParent(self, parent):
        self._parent = parent

    def pause(self):
        self._window.push_handlers(on_key_press=self._onKeyPress, on_mouse_press=self._onMousePress, on_draw=self._onDraw,
                                   on_resize=self._onResize)
        self._onResize(self._window.width, self._window.height)

    def _unpause(self):
        self._window.pop_handlers()
        self._parent.screenContinue()

    def _onKeyPress(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self._unpause()
        return True

    def _onMousePress(self, x, y, button, modifiers):
        return True

    def _onDraw(self):
        self._window.clear()
        self._pauseLabel.draw()
        return True

    def _onResize(self, width, height):
        self._pauseLabel.setButton(self._pauseLabelInfo[0] * self._window.width // self._pauseLabelInfo[1],
                                   self._pauseLabelInfo[2] *
                                   self._window.height // self._pauseLabelInfo[3],
                                   self._pauseLabelInfo[4] *
                                   self._window.width // self._pauseLabelInfo[5],
                                   self._pauseLabelInfo[6] * self._window.height // self._pauseLabelInfo[7])

import pyglet


class CCScreenTimeLabel:
    def __init__(self, x, window, gameInfo, batch, color):
        self._window = window
        self._gameInfo = gameInfo
        self._batch = batch
        self._seconds = None
        ribbonWidth = self._window.width // (self._gameInfo.playerCnt + 1)
        self._timeLabel = pyglet.text.Label('', font_name='Times New Roman', font_size=(self._window.height) // 20,
                                            color=color, x=x, y=(
                                                19 * self._window.height) // 20,
                                            width=ribbonWidth // 2, height=self._window.height // 10,
                                            anchor_x='center', anchor_y='center',
                                            group=pyglet.graphics.OrderedGroup(1), batch=None)

    def turnOn(self, seconds):
        self._seconds = seconds
        self._timeLabel.text = str(self._seconds)
        self._timeLabel.batch = self._batch

    def countDown(self):
        self._seconds -= 1
        self._timeLabel.text = str(self._seconds)

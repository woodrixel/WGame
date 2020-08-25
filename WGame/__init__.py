import pyglet
from pyglet.gl import *


def draw_rect(self, x, y, width, height, color):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]),
                         ("c3f", color))


class Window(pyglet.window.Window):

    def __init__(self, wwidth, wheight, text, event_handlers, fpslimit=60):
        super().__init__(width=wwidth, height=wheight, caption=text)

    def on_draw(self):
        self.clear()

    def start(self):
        pyglet.app.run()

    def exit(self):
        pyglet.app.exit()

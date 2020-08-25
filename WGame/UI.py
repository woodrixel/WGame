from pyglet import font


class UIObject:
    x = 0
    y = 0
    width = 0
    height = 0


class Font:
    size = 1


class Button(UIObject):
    text = ""
    font = 0
    action = 0

    def __init__(self, x, y, width, height, text, font, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.action = action

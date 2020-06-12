import pyglet
from pyglet.gl import *
import json


class WGame(pyglet.window.Window):
    wobjs = []
    delta_time = 0

    def __init__(self, wwidth, wheight, text, loopfunc, fpslimit=60, R=0.0, G=0.0, B=0.0):
        super().__init__(width=wwidth, height=wheight, caption=text)
        self.setbgcolor(R, G, B)
        pyglet.clock.schedule_interval(loopfunc, 1/fpslimit)

    def draw_rect(self, x, y, width, height, color):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]),
                             ("c3f", color))

    def on_draw(self):
        self.clear()
        for gobj in self.wobjs:
            if not type(gobj) == GameObject: continue
            gobj.position[0] += gobj.velocity[0]*self.delta_time
            gobj.position[1] += gobj.velocity[1]*self.delta_time

            gobj.collider_center_position = [gobj.position[0]+gobj.collider["center"][0], gobj.position[1]+gobj.collider["center"][1]]

        # TODO: Collisions (broken?)
        for gobj in self.wobjs:
            if not type(gobj) == GameObject: continue
            for cobj in self.wobjs:
                if cobj == gobj: continue
                if gobj.collider_center_position[0] > cobj.collider_center_position[0] and gobj.collider_center_position[0] < (cobj.collider_center_position[0] + gobj.collider["width"]):
                    if gobj.collider_center_position[1] > cobj.collider_center_position[1] and gobj.collider_center_position[1] < (cobj.collider_center_position[1] + gobj.collider["height"]):
                        gobj.on_collision(cobj)
                        cobj.on_collision(gobj)

        for wobj in self.wobjs:
            if wobj.data["objtype"] == "label":
                pyglet.text.Label(text=wobj.data["text"],
                                  font_name=wobj.data["font"],
                                  font_size=wobj.data["size"],
                                  x=wobj.data["x"], y=wobj.data["y"],
                                  color=wobj.data["color"],
                                  anchor_x=wobj.data["anchor_x"],
                                  anchor_y=wobj.data["anchor_y"]).draw()

            elif wobj.data["objtype"] == "button":
                self.draw_rect(wobj.data["x"], wobj.data["y"],
                               wobj.data["width"], wobj.data["height"],
                               wobj.cColor)
                pyglet.text.Label(text=wobj.data["text"],
                                  font_name=wobj.data["font"],
                                  font_size=wobj.data["size"],
                                  x=wobj.data["x"]+(wobj.data["width"]/2),
                                  y=wobj.data["y"]+(wobj.data["height"]/2),
                                  color=wobj.data["color"],
                                  anchor_x="center", anchor_y="center").draw()

            elif wobj.data["objtype"] == "gameobject":
                # TODO: Add suppport for transparency
                wobj.texture.blit(wobj.position[0], wobj.position[1])

    def on_mouse_press(self, x, y, button, modifiers):
        for wobj in self.wobjs:
            if wobj.data["objtype"] == "button":
                if x > wobj.data["x"] and x < (wobj.data["x"] + wobj.data["width"]):
                    if y > wobj.data["y"] and y < (wobj.data["y"] + wobj.data["height"]):
                        wobj.bAction()

    def on_mouse_motion(self, x, y, dx, dy):
        for wobj in self.wobjs:
            if wobj.data["objtype"] == "button":
                if x > wobj.data["x"] and x < (wobj.data["x"] + wobj.data["width"]):
                    if y > wobj.data["y"] and y < (wobj.data["y"] + wobj.data["height"]):
                        wobj.cColor = wobj.data["selbgcolor"]
                    else:
                        wobj.cColor = wobj.data["bgcolor"]
                else:
                    wobj.cColor = wobj.data["bgcolor"]

    def start(self):
        pyglet.app.run()

    def exit(self):
        pyglet.app.exit()

    def add(self, wobj):
        self.wobjs.append(wobj)
        wobj.index = len(self.wobjs)-1

    def remove(self, wobj):
        self.wobjs.pop(self.wobjs.index(wobj))

    def removeall(self):
        self.wobjs.clear()

    def setbgcolor(self, R, G, B, A=1.0):
        pyglet.gl.glClearColor(R, G, B, A)


class WObject:
    data = 0
    index = 0


class GuiObject(WObject):
    bAction = 0
    cColor = [0, 0, 0]

    def __init__(self, jsondata):
        self.data = json.loads(jsondata)
        try:
            if len(self.data["bgcolor"]) == 3:
                self.data["bgcolor"] *= 4
            if len(self.data["selbgcolor"]) == 3:
                self.data["selbgcolor"] *= 4
            self.cColor = self.data["bgcolor"]
        except KeyError:
            pass


class GameObject(WObject):
    velocity = [0.0, 0.0]
    position = [0.0, 0.0]
    collider_center_position = [0, 0]
    collider = 0
    texture = 0
    friction = 0

    def on_collision(self, col_obj):
        pass

    def __init__(self, jsondata):
        self.data = json.loads(jsondata)
        self.texture = pyglet.resource.image(self.data["texture"]).get_texture()
        self.texture.width = self.data["width"]
        self.texture.height = self.data["height"]
        self.friction = self.data["friction"]
        self.collider = self.data["collider"]

    pass

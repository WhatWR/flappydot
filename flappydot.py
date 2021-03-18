import tkinter as tk

from gamelib import Sprite, GameApp, Text
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
UPDATE_DELAY = 33
GRAVITY = 2.5
JUMP_VELOCITY = -20
PILLAR_SPEED = 5


class Dot(Sprite):
    def init_element(self):
        self.vy = -30
        self.is_started = False

    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY

    def start(self):
        self.is_started = True

    def jump(self):
        self.vu = JUMP_VELOCITY
        self.vy = self.vu

    def is_out_screen(self):
        if self.y > CANVAS_HEIGHT or self.y < -CANVAS_HEIGHT :
            return True
        else:
            return False


class PillarPair(Sprite):
    def init_element(self):
        self.is_started = False

    def update(self):
        if self.is_started:
            self.vx = -PILLAR_SPEED
            self.x += self.vx

    def start(self):
        self.is_started = True

    def game_over(self):
        self.is_started = False


    def is_hit(self, dot):
        return (self.x - 20 <= dot.x + 20 <= self.x + 20) and (dot.y >= self.y + 100 or dot.y <= self.y - 100)


class FlappyGame(GameApp):
    def create_sprites(self):
        self.dot = Dot(self, 'images/dot.png',
                       CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.elements.append(self.dot)
        self.pillar_pair = PillarPair(
            self, 'images/pillar-pair.png', CANVAS_WIDTH, CANVAS_HEIGHT // 2)
        self.elements.append(self.pillar_pair)

    def init_game(self):
        self.create_sprites()
        self.is_started = False

    def pre_update(self):
        pass

    def post_update(self):
        if self.dot.is_out_screen():
            self.game_over()

        if self.pillar_pair.is_hit(self.dot):
            self.game_over()

    def on_key_pressed(self, event):
        self.pillar_pair.start()
        self.dot.start()
        self.dot.jump()

    def game_over(self):
        self.dot.is_started = False
        self.pillar_pair.is_started = False
        self.pillar_pair.vx = 0




if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flappy dot Game")

    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()

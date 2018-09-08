from Storyboard import Storyboard
from Command import Command
from random import randint


class Effect:

    def __init__(self, command_factory, start_time, end_time):
        self.cf = command_factory
        self.start_time = Command.milliseconds(start_time)
        self.end_time = Command.milliseconds(end_time)
        self.sprites = list()

    def apply(self):
        pass

    def get_sprites(self):
        return self.sprites

    def append(self, sprite):
        self.sprites.append(sprite)

    @classmethod
    def random_playfield_point(cls):
        x = randint(-107, 747)
        y = randint(0, 480)
        return x, y



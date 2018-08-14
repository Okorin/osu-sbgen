from Command import Command
from random import randint


class Effect:
    def __init__(self, timing_points, start_time, end_time, *args):
        self.timing_points = timing_points
        self.start_time = Command.milliseconds(start_time)
        self.end_time = Command.milliseconds(end_time)
        self.sprites = list()

    def get_sprites(self):
        return self.sprites

    @classmethod
    def random_playfield_point(cls):
        x = randint(-107, 747)
        y = randint(0, 480)
        return x, y



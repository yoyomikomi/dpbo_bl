from ball import Ball
from stick import Stick
from table import Table
from physics import Physics
from score import Score

class Game:
    def __init__(self):
        self.balls = []
        self.stick = Stick()
        self.table = Table()
        self.score = Score()

    def start(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass
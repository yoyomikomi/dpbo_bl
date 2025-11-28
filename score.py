class Score:
    def __init__(self):
        self.score = 0

    def add(self, points):
        self.score += points
    
    def show(self):
        return self.score
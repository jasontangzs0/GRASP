

class Agent:
    def __init__(self, start_x, start_y):
        self.position = [start_x, start_y]
        self.energy = 0

    def move(self, direction):
        if direction == "up":
            self.position[0] -= 1
        elif direction == "down":
            self.position[0] += 1
        elif direction == "left":
            self.position[1] -= 1
        elif direction == "right":
            self.position[1] += 1

    def take_energy(self):
        self.energy += 1

    def report_position(self):
        return self.position

    def drop_all_energy(self):
        energy = self.energy
        self.energy = 0
        return energy
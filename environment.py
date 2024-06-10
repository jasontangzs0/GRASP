import numpy as np
import random
from collections import deque


class Cell:
    def __init__(self, obstacle=False):
        self.obstacle = obstacle
        self.energy = 0

    def place_energy(self):
        self.energy += 1

    def remove_energy(self):
        if self.energy > 0:
            self.energy -= 1

    def has_energy(self):
        return self.energy > 0

    def place_n_energy(self, n):
        self.energy += n

    def reset(self):
        self.energy = 0
        self.obstacle = False

    def set_obstacle(self):
        self.obstacle = True
        self.energy = 0


class GridEnvironment:
    def __init__(self, grid_size=11, steps=20, start=True):
        self.grid_size = grid_size
        self.grid = [[Cell() for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.steps = steps
        if start:
            self.distribute_energy()

    def take_energy(self, agent):
        x, y = agent.report_position()
        if self.grid[x][y].has_energy():
            self.grid[x][y].remove_energy()
            agent.take_energy()

    def distribute_energy(self, density=0.4):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if np.random.random() <= density:
                    self.grid[x][y].place_energy()

    def drop_all_energy(self, agent):
        x, y = agent.report_position()
        if agent.energy > 0:
            self.grid[x][y].place_n_energy(agent.drop_all_energy())

    def move_agent(self, agent, direction):
        row = agent.report_position()[0]
        col = agent.report_position()[1]
        if direction == "up":
            if row > 0 and not self.grid[row-1][col].obstacle:
                agent.move(direction)
                return True
            else:
                return False
        if direction == "down":
            if row < self.grid_size - 1 and not self.grid[row+1][col].obstacle:
                agent.move(direction)
                return True
            else:
                return False
        if direction == "left":
            if col > 0 and not self.grid[row][col-1].obstacle:
                agent.move(direction)
                return True
            else:
                return False
        if direction == "right":
            if col < self.grid_size - 1 and not self.grid[row][col+1].obstacle:
                agent.move(direction)
                return True
            else:
                return False
        if direction == "upleft":
            if row > 0 and col > 0 and not self.grid[row-1][col-1].obstacle:
                agent.move(direction)
                return True
            else:
                return False
        if direction == "upright":
            if row > 0 and col < self.grid_size - 1 and not self.grid[row-1][col+1].obstacle:
                agent.move(direction)
                return True
            else:
                return False
        if direction == "downleft":
            if row < self.grid_size - 1 and col > 0 and not self.grid[row+1][col-1].obstacle:
                agent.move(direction)
                return True
            else:
                return False
        if direction == "downright":
            if row < self.grid_size - 1 and col < self.grid_size - 1 and not self.grid[row+1][col+1].obstacle:
                agent.move(direction)
                return True
            else:
                return False

    def load_grid(self, grid_string):
        lines = grid_string.strip().split('\n')
        grid_start_index = 2

        # Reset grid
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.grid[x][y].reset()

        for x in range(self.grid_size):
            row_index = grid_start_index + (x * 2)
            row = lines[row_index]

            for y in range(self.grid_size):
                cell_index = 4 + (y * 4)
                cell_content = row[cell_index]

                if cell_content == 'E':
                    self.grid[x][y].place_energy()
                elif cell_content == 'O':
                    self.grid[x][y].set_obstacle()

    def get_opposite_direction(self, direction):
        opposite = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
            "upleft": "downright",
            "upright": "downleft",
            "downleft": "upright",
            "downright": "upleft"
        }
        return opposite[direction]

    def random_walk(self, agent, directions_num=4):
        if directions_num == 4:
            directions = ["up", "down", "left", "right"]
        else:
            directions = ["up", "down", "left", "right", "upleft", "upright", "downleft", "downright"]

        actions_taken = []
        all_action = []

        for _ in range(6):
            direction = random.choice(directions)
            self.move_agent(agent, direction)
            actions_taken.append(direction)
            all_action.append(direction)
            self.take_energy(agent)
            all_action.append('take')

        for direction in reversed(actions_taken):
            opposite_direction = self.get_opposite_direction(direction)
            self.move_agent(agent, opposite_direction)
            all_action.append(opposite_direction)

        self.drop_all_energy(agent)
        all_action.append('drop')
        return all_action

    def get_randomized_dict_items(self, d):
        items = list(d.items())
        random.shuffle(items)
        return items

    def find_nearest_energy_8(self, position):
        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
            "upleft": (-1, -1),
            "upright": (-1, 1),
            "downleft": (1, -1),
            "downright": (1, 1)
        }
        visited = set()
        queue = deque([(position, [])])  # Tuple of (cell_position, path)

        while queue:
            current_position, path = queue.popleft()
            x, y = current_position

            if self.grid[x][y].has_energy():
                return current_position, path

            visited.add(tuple(current_position))

            # Add neighboring cells to the queue
            for direction, (dx, dy) in self.get_randomized_dict_items(directions):
                neighbor_x, neighbor_y = x + dx, y + dy
                if 0 <= neighbor_x < self.grid_size and 0 <= neighbor_y < self.grid_size and \
                        (neighbor_x, neighbor_y) not in visited and not self.grid[neighbor_x][neighbor_y].obstacle:
                    queue.append(((neighbor_x, neighbor_y), path + [direction]))

        return None, []

    def find_nearest_energy(self, position):
        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }
        visited = set()
        queue = deque([(position, [])])

        while queue:
            current_position, path = queue.popleft()
            x, y = current_position

            if self.grid[x][y].has_energy():
                return current_position, path

            visited.add(tuple(current_position))

            # Add neighboring cells to the queue
            for direction, (dx, dy) in self.get_randomized_dict_items(directions):
                neighbor_x, neighbor_y = x + dx, y + dy
                if 0 <= neighbor_x < self.grid_size and 0 <= neighbor_y < self.grid_size and \
                   (neighbor_x, neighbor_y) not in visited and not self.grid[neighbor_x][neighbor_y].obstacle:
                    queue.append(((neighbor_x, neighbor_y), path + [direction]))

        return None, []

    def filter_out_take(self, my_list):
        return [action for action in my_list if action != 'take']

    def return_to_start(self, agent, path):
        reversed_path = [self.get_opposite_direction(direction) for direction in reversed(self.filter_out_take(path))]
        return_actions = []
        for direction in reversed_path:
            if self.steps <= 0:
                break
            self.move_agent(agent, direction)
            self.steps -= 1
            return_actions.append(direction)

        self.drop_all_energy(agent)
        return_actions.append('drop')
        return return_actions

    def greedy_search(self, agent, directions_num):
        result = []

        while self.steps > 0:
            start_position = agent.report_position()
            if directions_num == 8:
                nearest_energy_position, path = self.find_nearest_energy_8(start_position)
            else:
                nearest_energy_position, path = self.find_nearest_energy(start_position)

            if nearest_energy_position is None:
                break

            steps_needed = len(path)
            steps_needed_to_return = len(self.filter_out_take(result))

            if 2 * steps_needed + steps_needed_to_return + 1 + 1 > self.steps:
                result.extend(self.return_to_start(agent, result))
                return result

            for direction in path:
                if self.steps <= 0:
                    break
                self.move_agent(agent, direction.lower())
                self.steps -= 1
            result.extend(path)

            self.take_energy(agent)
            self.steps -= 1
            result.append('take')

        return result
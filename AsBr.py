import random

class AldousBroderMazeGenerator:

    def __init__(self, width, height):
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.maze = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.steps=0


    def add_border(self):
        for i in range(self.width):
            self.steps += 1
            self.maze[0][i] = 0
            self.maze[self.height - 1][i] = 0
        for i in range(self.height):
            self.maze[i][0] = 0
            self.maze[i][self.width - 1] = 0
            self.steps += 1

    def clear_inner_grid(self):
        for y in range(1, self.height - 1):
            self.steps += 1
            for x in range(1, self.width - 1):
                self.maze[y][x] = 0
                self.steps += 1

    def get_neighbors(self, x, y):
        neighbors = []
        if x > 1: neighbors.append((x - 2, y))
        if x < self.width - 3: neighbors.append((x + 2, y))
        if y > 1: neighbors.append((x, y - 2))
        if y < self.height - 3: neighbors.append((x, y + 2))
        self.steps += 1
        return neighbors

    def generate_maze(self, stepsList=[]):
        self.clear_inner_grid()
        self.add_border()


        current_x = random.randrange(1, self.width - 2, 2)
        current_y = random.randrange(1, self.height - 2, 2)

        self.maze[current_y][current_x] = 1
        visited_cells = 1
        total_cells = ((self.width - 1) // 2) * ((self.height - 1) // 2)

        while visited_cells < total_cells:
            neighbors = self.get_neighbors(current_x, current_y)
            unvisited_neighbors = [(nx, ny) for (nx, ny) in neighbors if self.maze[ny][nx] == 0]
            self.steps += 1

            if unvisited_neighbors:
                next_x, next_y = random.choice(unvisited_neighbors)
                self.maze[(current_y + next_y) // 2][(current_x + next_x) // 2] = 1
                self.maze[next_y][next_x] = 1
                current_x, current_y = next_x, next_y
                visited_cells += 1
                self.steps += 1
            else:
                while True:
                    current_x = random.randrange(1, self.width - 2, 2)
                    current_y = random.randrange(1, self.height - 2, 2)
                    if self.maze[current_y][current_x] == 1:
                        self.steps += 1
                        break

            yield self.maze

        yield self.maze
        print("")
        print(f"Total steps: {self.steps}")
        stepsList.append(self.steps)
        print(f"Average steps for Aldous Broder maze generation algorithm: {round(sum(stepsList) / len(stepsList), 2)}")





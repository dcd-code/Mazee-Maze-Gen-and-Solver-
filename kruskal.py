import random

class KruskalMazeGenerator:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[0 for _ in range(width)] for _ in range(height)]
        self.sets = {}
        self.walls = []
        self.steps = 0


    def _init_maze(self):

        for y in range(1, self.height, 2):
            self.steps += 1
            for x in range(1, self.width, 2):
                self.steps += 1

                cell = (y, x)
                self.maze[y][x] = 1
                self.sets[cell] = cell
                if y + 2 < self.height:
                    self.walls.append(((y + 1, x), (y + 2, x), (y, x)))
                if x + 2 < self.width:
                    self.walls.append(((y, x + 1), (y, x + 2), (y, x)))



    def find(self, cell):
        if self.sets[cell] != cell:
            self.sets[cell] = self.find(self.sets[cell])
            self.steps += 1
        return self.sets[cell]

    def join(self, cell1, cell2):
        root1 = self.find(cell1)
        root2 = self.find(cell2)
        if root1 != root2:
            self.steps += 1
            self.sets[root2] = root1

    def generate_maze(self, stepsList=[]):
        self._init_maze()
        random.shuffle(self.walls)

        for wall, cell1, cell2 in self.walls:
            self.steps += 1
            if self.find(cell1) != self.find(cell2):
                self.maze[wall[0]][wall[1]] = 1
                self.join(cell1, cell2)
                self.maze[cell2[0]][cell2[1]] = 1

                yield self.maze

        yield self.maze
        print("")
        print(f"Total steps: {self.steps}")
        stepsList.append(self.steps)

        print(f"Average steps for Kruskals maze generation algorithm: {round(sum(stepsList) / len(stepsList),2)}")
        print("Maze generated using Kruskal's algorithm.")




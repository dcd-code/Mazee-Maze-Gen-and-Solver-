import random
from collections import defaultdict
from typing import List, Tuple, Generator

class MazeGenerator:
    def __init__(self, num_width_cells: int, num_height_cells: int):
        self.num_width_cells = num_width_cells
        self.num_height_cells = num_height_cells
        self.width = self.num_width_cells
        self.height = self.num_height_cells
        self.maze = [[0] * self.width for _ in range(self.height)]
        self.visited = defaultdict(bool)
        self.unvisited_list = [(x, y) for x in range(1, self.width - 1, 2) for y in range(1, self.height - 1, 2)]
        self.directions = defaultdict(tuple)
        self.steps = 0

    def cellPath(self, node: Tuple[int, int]):
        self.steps += 1
        self.maze[node[1]][node[0]] = 1

    def unvisitedNode(self) -> Tuple[int, int]:
        self.steps += 1
        return self.unvisited_list[random.choice(range(len(self.unvisited_list)))]

    def visit(self, node: Tuple[int, int]):
        self.steps += 1
        if not self.visited[node]:
            self.unvisited_list.remove(node)
            self.visited[node] = True
            self.cellPath(node)

    def validNode(self, node: Tuple[int, int]) -> bool:
        self.steps += 1
        return 1 <= node[0] < self.width - 1 and 1 <= node[1] < self.height - 1

    def genNeighbours(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        self.steps += 1
        up_neighbor = (node[0], node[1] + 2)
        down_neighbor = (node[0], node[1] - 2)
        left_neighbor = (node[0] - 2, node[1])
        right_neighbor = (node[0] + 2, node[1])
        neighbor_list = [
            neighbor for neighbor in [up_neighbor, down_neighbor, left_neighbor, right_neighbor]
            if self.validNode(neighbor)
        ]
        return neighbor_list

    def randommov(self):
        self.steps += 1
        start_node = self.unvisitedNode()
        current_node = start_node
        neighbor_list = self.genNeighbours(current_node)

        while True:
            self.steps += 1
            chosen_neighbor = neighbor_list[random.choice(range(len(neighbor_list)))]
            self.directions[current_node] = chosen_neighbor

            if self.visited[chosen_neighbor]:
                break
            else:
                current_node = chosen_neighbor
                neighbor_list = self.genNeighbours(current_node)

        self.createPaths(start_node, current_node)

    def createPaths(self, start_node: Tuple[int, int], end_node: Tuple[int, int]):
        self.steps += 1
        current_node = start_node
        while True:
            self.steps += 1
            if current_node != end_node:
                next_node = self.directions[current_node]
                self.connectAdjnodes(current_node, next_node)
                current_node = next_node
            else:
                next_node = self.directions[current_node]
                self.connectAdjnodes(current_node, next_node)
                break

    def connectAdjnodes(self, node1: Tuple[int, int], node2: Tuple[int, int]):
        self.steps += 1
        if node1[0] > node2[0] and node1[1] == node2[1]:
            x = node1[0] - 1
            y = node1[1]
        elif node1[0] < node2[0] and node1[1] == node2[1]:
            x = node1[0] + 1
            y = node1[1]
        elif node1[1] > node2[1] and node1[0] == node2[0]:
            x = node1[0]
            y = node1[1] - 1
        elif node1[1] < node2[1] and node1[0] == node2[0]:
            x = node1[0]
            y = node1[1] + 1
        else:
            return

        self.visit(node1)
        self.visit(node2)
        self.cellPath((x, y))

    def generateMaze(self, stepsList= []) -> Generator[List[List[int]], None, None]:
        self.steps += 1
        self.maze = [[0] * self.width for _ in range(self.height)]
        self.visited = defaultdict(bool)
        self.unvisited_list = [(x, y) for x in range(1, self.width - 1, 2) for y in range(1, self.height - 1, 2)]

        for x in range(self.width):
            self.steps += 1
            self.maze[0][x] = 0
            self.maze[self.height - 1][x] = 0
        for y in range(self.height):
            self.steps += 1
            self.maze[y][0] = 0
            self.maze[y][self.width - 1] = 0

        self.start_node = self.unvisitedNode()
        self.visit(self.start_node)
        yield self.maze

        while self.unvisited_list:
            self.randommov()
            yield self.maze
        print("")
        print(f"Total steps: {self.steps}")
        stepsList.append(self.steps)
        print(f"Average steps for Wilson's maze generation algorithm: {sum(stepsList) / len(stepsList)}")


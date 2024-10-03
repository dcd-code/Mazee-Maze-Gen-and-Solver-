import random

def generate_maze(grid_state, steps=0, stepsList=[]):
    rows = len(grid_state)
    cols = len(grid_state[0])

    for y in range(rows):
        steps += 1
        for x in range(cols):
            steps += 1
            grid_state[y][x] = 0
    def inBounds(y, x):
        nonlocal steps
        steps += 1
        return 1 <= y < rows - 1 and 1 <= x < cols - 1


    def getNeighbors(y, x):
        nonlocal steps
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        neighbors = [(y + dy, x + dx) for dy, dx in directions if
                     inBounds(y + dy, x + dx) and grid_state[y + dy][x + dx] == 0]
        random.shuffle(neighbors)
        steps += 1
        return neighbors


    def carvePath(y, x):
        nonlocal steps
        grid_state[y][x] = 1
        steps += 1
        yield grid_state

        neighbors = getNeighbors(y, x)
        for ny, nx in neighbors:
            steps += 1
            if grid_state[ny][nx] == 0:
                grid_state[(y + ny) // 2][(x + nx) // 2] = 1
                yield grid_state
                yield from carvePath(ny, nx)
            else:

                steps += 1

    yield from carvePath(1, 1)

    print("")
    print(f"Total steps: {steps}")
    stepsList.append(steps)
    print(f"Average steps for Recursive Backtracker maze generation algorithm: {sum(stepsList)/len(stepsList)}")


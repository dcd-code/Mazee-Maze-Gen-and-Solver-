stepsList = []


def dfs(grid, start, end):
    stack = [(start, [start])]
    visited = set()
    steps = 0

    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        steps += 1

        y, x = current
        if grid[y][x] not in (2, 3):
            yield current, path, False
        if current == end:
            yield from ((node, path, True) for node in path)
            stepsList.append(steps)
            print("")
            print(f"Total steps taken: {steps}")
            print(stepsList)
            print(f"Average steps (DFS across runs): {round(sum(stepsList) / len(stepsList), 2)}")
            return

        for neighbor in get_neighbors(grid, y, x):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))


def get_neighbors(grid, y, x):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != 0:
            neighbors.append((ny, nx))
    return neighbors

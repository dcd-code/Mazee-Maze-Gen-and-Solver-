from collections import deque

stepsList = []

def bfs(grid, start_pos, end_pos):
    steps = 0
    rows, cols = len(grid), len(grid[0])
    start_y, start_x = start_pos
    end_y, end_x = end_pos

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start_pos, [])])
    visited = set()
    visited.add(start_pos)

    while queue:
        (current_y, current_x), path = queue.popleft()
        steps += 1

        if (current_y, current_x) == (end_y, end_x):
            final_path = path + [(current_y, current_x)]
            for pos in final_path:
                steps += 1
                yield pos, True

            stepsList.append(steps)
            print("")
            print("Path found")
            print(f"Total steps: {steps}")
            print(f"Average steps (BFS across runs): {round(sum(stepsList) / len(stepsList), 2)}")
            return

        for dy, dx in directions:
            ny, nx = current_y + dy, current_x + dx

            if 0 <= ny < rows and 0 <= nx < cols and (ny, nx) not in visited:
                if grid[ny][nx] != 0:
                    queue.append(((ny, nx), path + [(current_y, current_x)]))
                    visited.add((ny, nx))
                    yield (ny, nx), False

    # If we exit the loop without finding the end
    print("No path found.")
    return None

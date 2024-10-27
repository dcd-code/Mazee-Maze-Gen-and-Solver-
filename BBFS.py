from collections import deque

stepsList = []

def bbfs(grid, start_pos, end_pos):
    steps = 0
    rows, cols = len(grid), len(grid[0])
    start_y, start_x = start_pos
    end_y, end_x = end_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue_start = deque([(start_pos, [])])
    queue_end = deque([(end_pos, [])])
    visited_start = {start_pos: None}
    visited_end = {end_pos: None}

    def reconstruct_path(meeting_point):
        path_start = []
        current = meeting_point
        while current is not None:
            path_start.append(current)
            current = visited_start[current]
        path_start.reverse()

        path_end = []
        current = visited_end[meeting_point]
        while current is not None:
            path_end.append(current)
            current = visited_end[current]

        return path_start + path_end

    while queue_start and queue_end:
        current_start, path_start = queue_start.popleft()
        steps += 1
        if current_start in visited_end:
            final_path = reconstruct_path(current_start)
            for pos in final_path:
                steps += 1
                yield pos, True

            stepsList.append(steps)
            print("")
            print(f"Total steps: {steps}")
            print(f"Average steps (BBFS across runs): {round(sum(stepsList) / len(stepsList), 2)}")
            return

        for dy, dx in directions:
            ny, nx = current_start[0] + dy, current_start[1] + dx
            if 0 <= ny < rows and 0 <= nx < cols and (ny, nx) not in visited_start:
                if grid[ny][nx] != 0:
                    queue_start.append(((ny, nx), path_start + [current_start]))
                    visited_start[(ny, nx)] = current_start
                    yield (ny, nx), False

        current_end, path_end = queue_end.popleft()
        steps += 1

        if current_end in visited_start:
            final_path = reconstruct_path(current_end)
            for pos in final_path:
                steps += 1
                yield pos, True

            stepsList.append(steps)
            print("")
            print("Path found")
            print(f"Total steps: {steps}")
            print(f"Average steps (BBFS across runs): {round(sum(stepsList) / len(stepsList), 2)}")
            return

        for dy, dx in directions:
            ny, nx = current_end[0] + dy, current_end[1] + dx
            if 0 <= ny < rows and 0 <= nx < cols and (ny, nx) not in visited_end:
                if grid[ny][nx] != 0:
                    queue_end.append(((ny, nx), path_end + [current_end]))
                    visited_end[(ny, nx)] = current_end
                    yield (ny, nx), False

    # No path found; return None without yielding to prevent unpacking issues
    print("No path found.")
    return None

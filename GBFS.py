import heapq

stepsList = []


def h(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def gbfs(grid_state, start, end):
    steps = 0
    open_list = []
    heapq.heappush(open_list, (h(start, end), start))
    came_from = {}
    visited = set()

    while open_list:
        _, current = heapq.heappop(open_list)
        steps += 1

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()

            for step in path:
                steps += 1
                yield step, True

            stepsList.append(steps)
            print("")
            print(f"Total steps: {steps}")
            print(f"Average steps (GBFS across runs): {round(sum(stepsList) / len(stepsList), 2)}")
            return

        visited.add(current)

        neighbors = [
            (current[0] + dy, current[1] + dx)
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= current[0] + dy < len(grid_state) and 0 <= current[1] + dx < len(grid_state[0])
        ]

        for neighbor in neighbors:
            if grid_state[neighbor[0]][neighbor[1]] != 0 and neighbor not in visited:
                heapq.heappush(open_list, (h(neighbor, end), neighbor))
                came_from[neighbor] = current
                yield neighbor, False

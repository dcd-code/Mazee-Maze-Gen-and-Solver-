import heapq

stepsList = []
def dijkstra(grid_state, start_pos, end_pos, steps=0):
    rows, cols = len(grid_state), len(grid_state[0])
    distances = [[float('inf') for _ in range(cols)] for _ in range(rows)]
    distances[start_pos[0]][start_pos[1]] = 0

    priority_queue = [(0, start_pos)]
    visited = set()
    parent = {}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while priority_queue:
        current_distance, current_pos = heapq.heappop(priority_queue)
        if current_pos in visited:
            continue
        visited.add(current_pos)
        steps += 1

        if current_pos == end_pos:
            break

        for direction in directions:
            neighbor_y, neighbor_x = current_pos[0] + direction[0], current_pos[1] + direction[1]
            if 0 <= neighbor_y < rows and 0 <= neighbor_x < cols:
                if grid_state[neighbor_y][neighbor_x] != 0:
                    new_distance = current_distance + 1
                    if new_distance < distances[neighbor_y][neighbor_x]:
                        distances[neighbor_y][neighbor_x] = new_distance
                        heapq.heappush(priority_queue, (new_distance, (neighbor_y, neighbor_x)))
                        parent[(neighbor_y, neighbor_x)] = current_pos
                        yield (neighbor_y, neighbor_x), False

    path = []

    if end_pos in parent:
        node = end_pos
        while node != start_pos:
            steps += 1
            path.append(node)
            node = parent[node]
        path.append(start_pos)
        path.reverse()

    for pos in path:
        steps += 1
        yield pos, True


    stepsList.append(steps)
    print("")
    print(f"Total steps: {steps}")
    print(f"Steps list: {stepsList}")
    print(f"Average steps that Dijkstra's maze-solving algorithm took: {round(sum(stepsList) / len(stepsList), 2)}")

from queue import PriorityQueue

LINE_CHANGE_TIME = 500

def heuristic(data, station1, station2):
    lat1, lon1 = data[station1]['latitude'], data[station1]['longitude']
    lat2, lon2 = data[station2]['latitude'], data[station2]['longitude']
    return ((lat2 - lat1)**2 + (lon2 - lon1)**2)**0.5

def neighbors(graph, station):
    return graph[station].keys()

def cost(graph, from_station, to_station):
    connections = graph[from_station][to_station]
    return min(connection['time'] for connection in connections)

def searchRoute(data, lines_data, start_station, end_station):
    graph = {}
    for station, details in data.items():
        connections = details['connections']
        graph[station] = {}
        for line, line_details in connections.items():
            for connection in line_details['connections']:
                for dest_station, dest_details in connection.items():
                    if dest_station not in graph[station]:
                        graph[station][dest_station] = []
                    graph[station][dest_station].append({
                        'line': line,
                        'time': dest_details['time']
                    })                 
    frontier = PriorityQueue()
    frontier.put((0, start_station, None, []))
    came_from = {start_station: None}
    cost_so_far = {start_station: 0}
    current_line = {start_station: None}
    last_line_change = {start_station: None}

    while not frontier.empty():
        current_priority, current, line, last_line_change_stations = frontier.get()

        if current == end_station:
            break

        for next_station in neighbors(graph, current):
            for connection in graph[current][next_station]:
                new_cost = cost_so_far[current] + connection['time']
                if line is not None and connection['line'] != line:
                    new_cost += LINE_CHANGE_TIME
                    last_line_change_stations = [current] + last_line_change_stations[:1]

                if next_station not in cost_so_far or new_cost < cost_so_far[next_station]:
                    cost_so_far[next_station] = new_cost
                    priority = new_cost + heuristic(data, next_station, end_station)
                    frontier.put((priority, next_station, connection['line'], last_line_change_stations))
                    came_from[next_station] = current
                    current_line[next_station] = connection['line']
                    last_line_change[next_station] = last_line_change_stations

    # Backtrack to find the path
    path = []
    current = end_station
    while current is not None:
        path.append((current, current_line[current]))
        current = came_from[current]
    path.reverse()

    if path[-1][0] != start_station:  # If the path doesn't reach the start station
        last_line_change_stations = last_line_change[path[-1][0]]
        if len(last_line_change_stations) > 1:  # Check if there are at least two line change stations
            last_line_change_station = last_line_change_stations[1]  # Get the second last station where the line was changed
            print(last_line_change_stations)
            last_line = path[-1][1]  # Get the last line used
            other_lines = [line for line in data[last_line_change_station]['connections'].keys() if line != last_line]
            for line in other_lines:
                # Search again from the last line change station using a different line
                new_frontier = PriorityQueue()
                new_frontier.put((0, start_station, None, []))
                new_came_from = {start_station: None}
                new_cost_so_far = {start_station: 0}
                new_current_line = {start_station: None}
                new_last_line_change = {start_station: None}
                
                while not new_frontier.empty():
                    new_current_priority, new_current, new_line, new_last_line_change_stations = new_frontier.get()

                    if new_current == end_station:
                        break

                    for new_next_station in neighbors(graph, new_current):
                        for new_connection in graph[new_current][new_next_station]:
                            new_new_cost = new_cost_so_far[new_current] + new_connection['time']
                            if new_line is not None and new_connection['line'] != new_line:
                                new_new_cost += LINE_CHANGE_TIME
                                new_last_line_change_stations = [new_current] + new_last_line_change_stations[:1]

                            if new_next_station not in new_cost_so_far or new_new_cost < new_cost_so_far[new_next_station]:
                                new_cost_so_far[new_next_station] = new_new_cost
                                new_priority = new_new_cost + heuristic(data, new_next_station, end_station)
                                new_frontier.put((new_priority, new_next_station, new_connection['line'], new_last_line_change_stations))
                                new_came_from[new_next_station] = new_current
                                new_current_line[new_next_station] = new_connection['line']
                                new_last_line_change[new_next_station] = new_last_line_change_stations

                # Backtrack to find the new path
                new_path = []
                new_current = end_station
                while new_current is not None:
                    new_path.append((new_current, new_current_line[new_current]))
                    new_current = new_came_from[new_current]
                new_path.reverse()

                # Check if the new path is more efficient
                if cost_so_far[end_station] < new_cost_so_far[end_station]:
                    path = new_path
                    print("new path better")

    print(path)

    return came_from, cost_so_far, graph, cost_so_far, current_line

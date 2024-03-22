from queue import PriorityQueue
import sys

LINE_CHANGE_TIME = 500

def heuristic(data, station1, station2, currentLine, end_station):
    lat1, lon1 = data[station1]['latitude'], data[station1]['longitude']
    lat2, lon2 = data[station2]['latitude'], data[station2]['longitude']
    
    # Calculate the Euclidean distance between stations
    euclidean_distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5
    
    # Penalize line changes if the current line is different from the line needed to reach the destination
    if end_station in data:
        end_connections = data[end_station].get('connections', {})
        if end_connections:
            end_line = next(iter(end_connections))
            if currentLine != end_line:
                euclidean_distance *= 10000
                print("Multiplied")
    
    return euclidean_distance



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
    frontier.put((0, start_station, None))
    came_from = {start_station: None}
    cost_so_far = {start_station: 0}
    current_line = {start_station: None}


    while not frontier.empty():
        current_priority, current, line = frontier.get()

        if current == end_station:
            break

        for next_station in neighbors(graph, current):
            for connection in graph[current][next_station]:
                new_cost = cost_so_far[current] + connection['time']
                if connection['line'] != line:
                    new_cost += LINE_CHANGE_TIME

                if next_station not in cost_so_far or new_cost < cost_so_far[next_station]:
                    cost_so_far[next_station] = new_cost
                    priority = new_cost + (heuristic(data, next_station, end_station, connection['line'], end_station))
                    frontier.put((priority, next_station, connection['line']))
                    came_from[next_station] = current
                    current_line[next_station] = connection['line']
    return came_from, cost_so_far, graph, cost_so_far, current_line
from queue import PriorityQueue

def print_progress_bar(current, total, bar_length=50):
    percent = float(current) / total
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    print(f"\rProgress: [{arrow + spaces}] {int(round(percent * 100))}%", end='')

def searchRoute(data, lines_data, start_station, end_station, max_attempts=100000):
    graph = {}
    
    # Initialize the graph based on provided data
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
    def find_paths(start_station, end_station):
        #piority queue stores (total_time, current_station, path, last_line, visited)
        pq = PriorityQueue()
        #initializing the priority queue with the start station
        pq.put((0, start_station, [], None, set(start_station)))
        #attempts counter
        attempts = 0
        #while the priority queue is not empty and the attempts are less than the max attempts
        while not pq.empty() and attempts < max_attempts:
            #get the current station and path from the priority queue
            total_time, current_station, path, last_line, visited = pq.get()
            #if the current station is the end station return the path and the total time
            if current_station == end_station:
                #return the path and the total time
                return path + [end_station], total_time
            #for each station linked to the current station
            for next_station in graph[current_station]:
                #for each line linking the current station to the next station
                for connection in graph[current_station][next_station]:
                    #store the line name and the time
                    line = connection['line']
                    time = connection['time']
                    #if the next station has not been visited
                    if next_station not in visited:
                        #create a new visited set with the next station added
                        new_visited = visited.copy()
                        #add the next station to the new visited set
                        new_visited.add(next_station)
                        #calculate the new total time
                        new_total_time = total_time + time + (0 if last_line == line else 15)
                        #create a new path with the next station added
                        new_path = path + [(current_station, line, time)]
                        #add the new total time, next station, new path, line and new visited to the priority queue
                        pq.put((new_total_time, next_station, new_path, line, new_visited))
            #increment the attempts counter
            attempts += 1
        
        return [], float('inf')  # No path found or max attempts reached
    
    shortest_path, total_time = find_paths(start_station, end_station)
    return shortest_path, total_time
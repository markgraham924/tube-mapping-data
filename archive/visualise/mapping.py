import json
import heapq

data = json.load(open('./stations_formatted_updated v4.json', 'r', encoding='utf-8'))

def dijkstra(data, start, end):
    
    distances = {station: float('infinity') for station in data}
    distances[start] = 0

    
    previous = {station: (None, None) for station in data}  

    
    pq = [(0, start, None)]

    while pq:
        
        current_distance, current_station, last_line = heapq.heappop(pq)

        
        if current_station == end:
            break

        
        for line, line_info in data[current_station]["connections"].items():
            for connection in line_info["connections"]:
                for station, details in connection.items():
                    time = details["time"]
                    line_change_penalty = 500 if line != last_line and last_line is not None else 0
                    distance = current_distance + time + line_change_penalty

                    
                    if distance < distances[station]:
                        distances[station] = distance
                        previous[station] = (current_station, line)  
                        heapq.heappush(pq, (distance, station, line))

    
    path = []
    current = end
    while current:
        path.append(current)
        current, _ = previous[current]
    path.reverse()

    return path, distances[end]


start_station = "Acton Town"
end_station = "West Kensington"  
path, distance = dijkstra(data, start_station, end_station)
print(path, distance)
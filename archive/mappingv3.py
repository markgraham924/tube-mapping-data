import json
import heapq
import math


data = json.load(open('./stations_formatted_updated v4.json', 'r', encoding='utf-8'))

def physicalDistance(station1, station2):
    R=6371.0
    lat1, lon1 = data[station1]['latitude'], data[station1]['longitude']
    lat2, lon2 = data[station2]['latitude'], data[station2]['longitude']
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def heuristic(station1, station2):
    
    lat1, lon1 = data[station1]['latitude'], data[station1]['longitude']
    lat2, lon2 = data[station2]['latitude'], data[station2]['longitude']
    return ((lat2 - lat1)**2 + (lon2 - lon1)**2)**0.5

def a_star_with_forced_start_line(data, start, goal, change_penalty, pm25):
    
    best_path, best_cost = None, float('infinity')

    initial_lines = data[start]['connections'].keys()
    for initial_line in initial_lines:
        path, cost, pm25_total = a_star_modified(data, start, goal, change_penalty, pm25, initial_line)
        
        if cost < best_cost:
            best_path, best_cost = path, cost
    
    return best_path, best_cost, pm25_total

def a_star_modified(data, start, goal, change_penalty, pm25, forced_line=None):
    open_set = [(0, 0, start, None, 0)]  
    came_from = {}
    g_score = {station: float('infinity') for station in data}
    g_score[start] = 0
    pm25_exposure = {station: 0 for station in data}  

    while open_set:
        _, current_cost, current_station, last_line, current_pm25_exposure = heapq.heappop(open_set)

        if current_station == goal:
            return reconstruct_path(came_from, start, goal), current_cost, current_pm25_exposure

        for line, line_info in data[current_station]['connections'].items():
            if forced_line and current_station == start and line != forced_line:
                continue

            pm25_line_level = line_info.get('PM2.5', 0)  

            for connection in line_info['connections']:
                for next_station, details in connection.items():
                    time = details.get('time', 0)
                    #proposed_g_score = current_cost + ((pm25 * pm25_line_level) + ((100 - pm25) * time))
                    proposed_g_score = current_cost + (time * pm25_line_level)
                    line_change_penalty = change_penalty if line != last_line and last_line is not None else 0
                    proposed_g_score += line_change_penalty
                    
                    
                    proposed_pm25_exposure = current_pm25_exposure + (pm25_line_level)

                    if proposed_g_score < g_score.get(next_station, float('infinity')):
                        came_from[next_station] = (current_station, line)
                        g_score[next_station] = proposed_g_score
                        pm25_exposure[next_station] = proposed_pm25_exposure  
                        heapq.heappush(open_set, (proposed_g_score, proposed_g_score, next_station, line, proposed_pm25_exposure))
                        
    return None, float('infinity'), 0


def reconstruct_path(came_from, start, goal):
    path_with_changes = []
    current_station = goal
    last_line = None
    segments = []

    
    while current_station != start:
        prev_station, line_used = came_from[current_station]
        segments.append((prev_station, line_used, current_station))
        current_station = prev_station

    segments.reverse()

    
    for i, (from_station, line, to_station) in enumerate(segments):
        
        if i == 0:
            path_with_changes.append(f"Start at {from_station}, take {line} towards {to_station}")
            last_line = line
        else:
            
            if line != last_line:
                path_with_changes.append(f"Change at {from_station} to {line}, continue towards {to_station}")
                last_line = line
            
            if to_station == goal and segments[i-1][2] != goal:
                path_with_changes.append(f"Arrive at {to_station} via {line}")

    return path_with_changes



def find_best_path(data, start, goal, pm25):
    path, cost, pm25_total = a_star_with_forced_start_line(data, start, goal, 50, pm25)
    walking_distance = physicalDistance(start, goal)

    print(f"Total distance: {walking_distance:.2f} km")
    if path:
        print("Best path found:")
        for step in path:
            print(step)
        print(f"Total cost: {cost}")
        print(f"Total PM2.5 exposure: {pm25_total:.2f}")
    else:
        print("No path found.")
    return path




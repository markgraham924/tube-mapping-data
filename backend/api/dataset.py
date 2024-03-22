import json
from mapping import searchRoute


ZONES = [1, 2, 3, 4, 5, 6, 7, 8, 9]
zone_floats = set(float(zone) for zone in ZONES)


with open('./backend/api/stations_formatted_updated v4.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
with open('./backend/api/lines.json', 'r', encoding='utf-8') as file:
    lines_data = json.load(file)


#function to return a single station and it's data
def station(station_name):
    response = data.get(station_name)
    if response:
        return station_name, response, 200
    else:
        return station_name, {'error': 'Station not found. Please check the spelling and try again.'}, 400

#returns a list of all station names
def stations(limit=None, zones=None):
    if zones:
        zone_floats = set(float(zone) for zone in zones)
        station_names = [
            station for station in data 
            if any(zone <= float(data[station].get('zone', 0)) <= zone + 0.5 for zone in zone_floats)
        ]
    else:
        station_names = list(data.keys())

    station_names = station_names[:limit] if limit is not None and limit > 0 else station_names
    
    return station_names, 200

#returns a list of all lines
def lines():
    lines = list(lines_data.keys())
    return lines, 200

def reconstruct_path(came_from, current_line, start, end):
    current = end
    path = [(current, current_line[current])]  # Include the line for each station
    while current != start:
        current = came_from[current]
        line = current_line[current]
        path.append((current, line))
    path.reverse()  # Reverse the path to start from the beginning
    return path

def getRoute(start_station, end_station):
    return(searchRoute(data, lines_data, start_station, end_station)) # came_from, cost_so_far, graph, cost_so_far, current_line
    #path = reconstruct_path(came_from, current_line, start_station, end_station)
    #return path, cost_so_far[end_station]
    
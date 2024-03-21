import json
import pygame
import csv
import sys

pygame.init()

window_size = [1080, 720]
background_color = (255, 255, 255)
padding = 50
font = pygame.font.Font(None, 16)

screen = pygame.display.set_mode(window_size)



temp_data = json.load(open('./stations_formatted_updated v4.json', 'r', encoding='utf-8'))

data = {}



lines = {}
with open('./preprocess/dataset/lines.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        lines[row['name']] = "#" + row['colour']

keys = list(lines.keys())  
row_index = 8

lineName = keys[row_index]  
pygame.display.set_caption(lineName)
for station, details in temp_data.items():
    if any(lineName in line for line in details.get("connections", {})):
        data[station] = details
        
data = temp_data

def scale(value, min_old, max_old, min_new, max_new):
    return ((value - min_old) / (max_old - min_old)) * (max_new - min_new) + min_new


def prepare_stations(data):
    stations_prepared = {}
    for station, details in data.items():
        pm25_values = []
        for line in details.get("connections", {}).values():
            if "PM2.5" in line:  
                pm25_values.append(line["PM2.5"])

        
        max_pm25 = max(pm25_values, default=0)
        stations_prepared[station] = {
            "latitude": details["latitude"],
            "longitude": details["longitude"],
            "connections": details.get("connections", {}),
            "color": None  ,
            "pm25": max_pm25
        }
        for line in details.get("connections", {}):
            if line in lines:
                stations_prepared[station]["color"] = lines[line]
                break  
    return stations_prepared

stations_with_color = prepare_stations(data)


def find_min_max_lat_lon(data):
    
    min_lat, max_lat = float('inf'), float('-inf')
    min_lon, max_lon = float('inf'), float('-inf')

    for station, details in data.items():
        lat = details["latitude"]
        lon = details["longitude"]

        
        if lat < min_lat:
            min_lat = lat
        if lat > max_lat:
            max_lat = lat

        
        if lon < min_lon:
            min_lon = lon
        if lon > max_lon:
            max_lon = lon

    
    print(f"Latitude range: {min_lat} to {max_lat}, Longitude range: {min_lon} to {max_lon}")
    
    return min_lat, max_lat, min_lon, max_lon



min_lat, max_lat, min_lon, max_lon = find_min_max_lat_lon(stations_with_color)

def lat_lon_to_screen(lat, lon):
    x = scale(lon, min_lon, max_lon, padding, window_size[0] - padding)
    y = scale(lat, min_lat, max_lat, window_size[1] - padding, padding)
    return int(x), int(y)

def draw_connections(screen, stations_with_color, data, lines):
    for station_name, station_details in stations_with_color.items():
        if station_name in data and "connections" in data[station_name]:
            start_x, start_y = lat_lon_to_screen(station_details["latitude"], station_details["longitude"])
            for line_name, connection_details in data[station_name]["connections"].items():
                if line_name in lines:  
                    line_color = pygame.Color((lines[line_name]))
                    for connected_station_detail in connection_details["connections"]:
                        for connected_station_name, _ in connected_station_detail.items():
                            if connected_station_name in stations_with_color:  
                                end_x, end_y = lat_lon_to_screen(
                                    stations_with_color[connected_station_name]["latitude"], 
                                    stations_with_color[connected_station_name]["longitude"])
                                pygame.draw.line(screen, line_color, (start_x, start_y), (end_x, end_y), 2)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(background_color)

    
    draw_connections(screen, stations_with_color, data, lines)


    
    for station, details in stations_with_color.items():
        x, y = lat_lon_to_screen(details["latitude"], details["longitude"])
        color = details["color"] if details["color"] else "#000000"
        pygame.draw.circle(screen, pygame.Color(color), (x, y), 5)
        if details["pm25"] is not None:
            
            
            text_surface = font.render(f"{station}", True, (0, 0, 0))
            screen.blit(text_surface, (x - 10, y))
    pygame.display.flip()

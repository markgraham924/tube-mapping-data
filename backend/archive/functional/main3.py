from mappingv3 import find_best_path
import json

data = json.load(open('./stations_formatted_updated v4.json', 'r', encoding='utf-8'))

start_station = "Euston"
goal_station = "Turnham Green"
path = find_best_path(data, start_station, goal_station, 0)

print(path)

import json
import pygame
import csv
import sys

pygame.init()

window_size = [1920, 1080]
background_color = (255, 255, 255)
padding = 50
font = pygame.font.Font(None, 16)

screen = pygame.display.set_mode(window_size)

zoom = 0.5

x_offset = 0
y_offset = 0



data = json.load(open('./stations_formatted_updated v4.json', 'r', encoding='utf-8'))

lines = {}
with open('./preprocess/dataset/lines.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        lines[row['name']] = "#" + row['colour']

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


def find_min_max_lat_lon_for_path(data, path):
    min_lat, max_lat = float('inf'), float('-inf')
    min_lon, max_lon = float('inf'), float('-inf')

    
    stations_in_path = set([segment[0] for segment in path] + [segment[2] for segment in path])

    for station in stations_in_path:
        details = data.get(station, {})
        lat = details.get("latitude")
        lon = details.get("longitude")

        if lat is not None and lon is not None:
            if lat < min_lat: min_lat = lat
            if lat > max_lat: max_lat = lat
            if lon < min_lon: min_lon = lon
            if lon > max_lon: max_lon = lon

    return min_lat, max_lat, min_lon, max_lon



min_lat, max_lat, min_lon, max_lon = find_min_max_lat_lon_for_path(data, path)

def find_uniform_scale(min_lat, max_lat, min_lon, max_lon, window_size, padding):
    
    lat_range = max_lat - min_lat
    lon_range = max_lon - min_lon
    
    
    display_width = window_size[0] - 2 * padding
    display_height = window_size[1] - 2 * padding

    
    scale_x = display_width / lon_range
    scale_y = display_height / lat_range

    
    uniform_scale = min(scale_x, scale_y)

    
    MIN_SCALE = 0.01  
    uniform_scale = max(uniform_scale, MIN_SCALE)

    return uniform_scale

uniform_scale = find_uniform_scale(min_lat, max_lat, min_lon, max_lon, window_size, padding)

def lat_lon_to_screen(lat, lon):
    
    x = (padding + (lon - min_lon) * uniform_scale * zoom)+(window_size[0]/2- x_offset)
    y = (window_size[1] - padding - (lat - min_lat) * uniform_scale * zoom - y_offset)

    return int(x), int(y)

def draw_connections(screen, stations_with_color, data, lines, path):
    
    for station_name, station_details in stations_with_color.items():
        if "connections" in data[station_name]:
            start_x, start_y = lat_lon_to_screen(station_details["latitude"], station_details["longitude"])
            for line_name, connection_details in data[station_name]["connections"].items():
                line_color = pygame.Color(lines[line_name]) if line_name in lines else pygame.Color("#000000")
                for connected_station_detail in connection_details["connections"]:
                    for connected_station_name, _ in connected_station_detail.items():
                        if connected_station_name in stations_with_color:  
                            end_x, end_y = lat_lon_to_screen(
                                stations_with_color[connected_station_name]["latitude"], 
                                stations_with_color[connected_station_name]["longitude"])
                            pygame.draw.line(screen, line_color, (start_x, start_y), (end_x, end_y), 1)  

    
    for segment in path:
        start_station, line, end_station = segment  
        if start_station in stations_with_color and end_station in stations_with_color:
            start_details = stations_with_color[start_station]
            end_details = stations_with_color[end_station]

            start_x, start_y = lat_lon_to_screen(start_details["latitude"], start_details["longitude"])
            end_x, end_y = lat_lon_to_screen(end_details["latitude"], end_details["longitude"])

            
            pygame.draw.line(screen, lines[line], (start_x, start_y), (end_x, end_y), 6)  



def draw_stations(screen, stations_with_color, path):
    
    for station, details in stations_with_color.items():
        x, y = lat_lon_to_screen(details["latitude"], details["longitude"])
        
        pygame.draw.circle(screen, pygame.Color("#000000"), (x, y), 5)
        text_surface = font.render(f"{station}", True, (0, 0, 0))
        screen.blit(text_surface, (x + 10, y))
        if (zoom > 3):
            if details["pm25"] is not None:
                text_surface = font.render(f"{details['pm25']}", True, (0, 0, 0))
                screen.blit(text_surface, (x - 10, y+10))

    
    path_stations = set([segment[0] for segment in path] + [segment[2] for segment in path])
    for station in path_stations:
        if station in stations_with_color:
            details = stations_with_color[station]
            x, y = lat_lon_to_screen(details["latitude"], details["longitude"])
            
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 7)  



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_offset += 10  
            elif event.key == pygame.K_RIGHT:
                x_offset -= 10  
            elif event.key == pygame.K_UP:
                y_offset += 10  
            elif event.key == pygame.K_DOWN:
                y_offset -= 10  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  
                zoom_change = min(2 - zoom, 0.1)
            elif event.button == 5:  
                zoom_change = max(0.1 - zoom, -0.1)
            else:
                continue  

            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            center_x, center_y = window_size[0] / 2, window_size[1] / 2
            dx = (mouse_x - center_x) / (uniform_scale * zoom)
            dy = (mouse_y - center_y) / (uniform_scale * zoom)

            
            zoom += zoom_change

            
            if zoom_change > 0:  
                x_offset -= dx * zoom_change * 10
                y_offset += dy * zoom_change * 10
            elif zoom_change < 0:  
                x_offset += dx * (-zoom_change) * 10
                y_offset -= dy * (-zoom_change) * 10

    screen.fill(background_color)

    draw_connections(screen, stations_with_color, data, lines, path)
    draw_stations(screen, stations_with_color, path)
        
    pygame.display.flip()

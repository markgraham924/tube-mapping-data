from mapping import searchRoute
import pygame
from dataset import data, lines_data, getRoute
import sys
import requests
import json

with open('./api/lines.json', 'r', encoding='utf-8') as file:
    lines_colors = json.load(file)

def visualiseRoute(data, pathGiven):
    path = pathGiven

    
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Tube Map Route Visualization')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    
    min_lat = min(station['latitude'] for station in data.values())
    max_lat = max(station['latitude'] for station in data.values())
    min_lon = min(station['longitude'] for station in data.values())
    max_lon = max(station['longitude'] for station in data.values())

    def lat_lon_to_screen(lat, lon):
        
        norm_x = (lon - min_lon) / (max_lon - min_lon)
        norm_y = (lat - min_lat) / (max_lat - min_lat)
        screen_x = norm_x * (screen.get_width() - 100) + 50  
        screen_y = (1 - norm_y) * (screen.get_height() - 100) + 50  
        return int(screen_x), int(screen_y)
    
    def draw_all_stations():
        for station, details in data.items():
            pos = lat_lon_to_screen(details['latitude'], details['longitude'])
            
            pygame.draw.circle(screen, (200, 200, 200), pos, 5)  
            
            font = pygame.font.Font(None, 8)
            text = font.render(station, True, (128, 128, 128))  
            screen.blit(text, (pos[0] + 5, pos[1]))

    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))
        draw_all_stations()
        first = True
        size = 1
        color = (255, 0, 0)
        previous_line = None
        for i, item in enumerate(pathGiven[:-1]):  
            station_from, line, _ = item
            station_to = pathGiven[i + 1][0] if i + 1 < len(pathGiven) - 1 else pathGiven[-1]
            
            line_color_hex = lines_colors.get(line, "000000")
            line_color = pygame.Color(line_color_hex)
            
            from_pos = lat_lon_to_screen(data[station_from]['latitude'], data[station_from]['longitude'])
            to_pos = lat_lon_to_screen(data[station_to]['latitude'], data[station_to]['longitude'])

            pygame.draw.line(screen, line_color, from_pos, to_pos, 5)
            
            if first:
                size = 10
                first = False
                color = (0, 255, 20)
                text = font.render(station_from, True, (0, 0, 0))
                screen.blit(text, (from_pos[0] + 15, from_pos[1]))
            pygame.draw.circle(screen, color, from_pos, size)
            if line != previous_line and previous_line is not None:
                text = font.render(station_from, True, (0, 0, 0))
                screen.blit(text, (from_pos[0] + 15, from_pos[1]))
                pygame.draw.circle(screen, pygame.Color(0,0,255), from_pos, 10)  

            size = 5
            color = (20, 20, 20)
            previous_line = line

        
        if pathGiven:
            last_station = pathGiven[-1] if isinstance(pathGiven[-1], str) else pathGiven[-1][0]
            if last_station in data:  
                last_pos = lat_lon_to_screen(data[last_station]['latitude'], data[last_station]['longitude'])
                pygame.draw.circle(screen, (255, 0, 0), last_pos, 10)
                text = font.render(last_station, True, (0, 0, 0))
                screen.blit(text, (last_pos[0] + 15, last_pos[1]))

        pygame.display.flip()  
        clock.tick(60)  



url = "http://127.0.0.1:5000/api/findRoute/West Ruislip/Ruislip"
response = requests.get(url)
if response.status_code == 200:
    route_info = response.json()
    
    path_given = route_info.get("path")
    if path_given:
        visualiseRoute(data, path_given)
    else:
        print("Path not found in the response.")
else:
    print(f"Failed to get route. Status code: {response.status_code}")

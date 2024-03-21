import json
import pygame
import csv
import sys

pygame.init()


window_size = [1920, 1080]
background_color = (255, 255, 255)  
padding = 50  


screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("London Underground Stations")

data = json.load(open('./preprocess/stations_formatted.json', 'r', encoding='utf-8'))


lines = {}
with open('./preprocess/dataset/lines.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        lines[row['name']] = row['colour']

def scale(value, min_old, max_old, min_new, max_new):
    return ((value - min_old) / (max_old - min_old)) * (max_new - min_new) + min_new



def prepare_stations(data):
    stations_prepared = {}
    for station, details in data.items():
        if "connections" in details:
            for line in details["connections"]:
                if line in lines:
                    stations_prepared[station] = {
                        "latitude": details["latitude"],
                        "longitude": details["longitude"],
                        "color": lines[line]
                    }
                    break  
    return stations_prepared


stations_with_color = prepare_stations(data)

def lat_lon_to_screen(lat, lon, min_lat, max_lat, min_lon, max_lon):
    min_lat, max_lat = 51.28, 51.686
    min_lon, max_lon = -0.510, 0.334
    x = scale(lon, min_lon, max_lon, padding, window_size[0] - padding)
    y = scale(lat, min_lat, max_lat, window_size[1] - padding, padding)  
    return int(x), int(y)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    screen.fill(background_color)
    
    
    for station, details in stations_with_color.items():
        x, y = lat_lon_to_screen(details["latitude"], details["longitude"], 51.28, 51.686, -0.510, 0.334) 
        color = "#" + details["color"]
        pygame.draw.circle(screen, pygame.Color(color), (x, y), 5)
    
    pygame.display.flip()
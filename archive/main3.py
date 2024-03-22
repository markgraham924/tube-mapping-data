from mappingv3 import find_best_path
import json

data = json.load(open('./stations_formatted_updated v4.json', 'r', encoding='utf-8'))

start_station = "Sloane Square"
goal_station = "East Finchley"
print(find_best_path(data, start_station, goal_station, 100, True))
find_best_path(data, start_station, goal_station, 0, True)
import csv
import json

stations = {}
lines = {}

station_names = {}
with open('./preprocess/dataset/stations.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        station_names[row['id']] = row['name']


with open('./preprocess/dataset/lines.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        lines[row['line']] = {
            'name': row['name'],
            'colour': row['colour'],
            'stripe': row['stripe'] if 'stripe' in row else None
        }

with open('./preprocess/dataset/stations.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        station_name = row['name']
        stations[station_name] = {
            'latitude': float(row['latitude']),
            'longitude': float(row['longitude']),
            'display_name': row['display_name'] if 'display_name' in row else None,
            'zone': row['zone'],
            'total_lines': int(row['total_lines']),
            'rail': int(row['rail']),
            'connections': {}
        }

with open('./preprocess/dataset/connections.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        station1_name = station_names[row['station1']]
        station2_name = station_names[row['station2']]
        line_id = row['line']
        time = int(row['time'])
        
        line_name = lines[line_id]['name']
        if line_name not in stations[station1_name]['connections']:
            pm25 = input("Enter PM2.5 value for " + station1_name + " on line " + line_name + ": ")
            if (pm25):
                pm25 = float(pm25)
            stations[station1_name]['connections'][line_name] = {"connections": [], "PM2.5": pm25}
        stations[station1_name]['connections'][line_name]["connections"].append({station2_name: {"time": time}})


with open('stations_formatted.json', 'w', encoding='utf-8') as file:
    json.dump(stations, file, indent=4)

print("Formatted JSON conversion is complete.")

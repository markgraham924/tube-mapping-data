import json

data = json.load(open('./preprocess/stations_formatted.json', 'r', encoding='utf-8'))

def find_pm25_values(station_name, visited=None):
    if visited is None:
        visited = set()
    visited.add(station_name)
    
    station_details = data[station_name]
    pm25_values = []
    
    for connection in station_details["connections"].values():
        if connection["PM2.5"]:
            pm25_values.append(connection["PM2.5"])
        else:
            for next_station in connection["connections"]:
                for next_station_name, _ in next_station.items():
                    if next_station_name not in visited:
                        pm25_values.extend(find_pm25_values(next_station_name, visited))
    
    return pm25_values

#get the line averages
line_averages = {}
for station, details in data.items():
    for line in details["connections"].keys():
        if line not in line_averages:
            line_averages[line] = []


for station, details in data.items():
    for line, connection in details["connections"].items():
        if connection["PM2.5"] == "":
            pm25_values = find_pm25_values(station)
            if pm25_values:
                average_pm25 = float(sum(pm25_values) / len(pm25_values))
                connection["PM2.5"] = average_pm25
                line_averages[line].append(average_pm25)
        else:
            
            line_averages[line].append(float(connection["PM2.5"]))


for line, values in line_averages.items():
    if values:
        line_averages[line] = sum(values) / len(values)
    else:
        line_averages[line] = None  




for station, details in data.items():
    for line, connection in details["connections"].items():
        if connection["PM2.5"] == "":
            connection["PM2.5"] = float(int(line_averages[line]))




file_path = './preprocess/stations_formatted_updated.json'

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Data successfully updated and written to", file_path)
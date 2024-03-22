import json


data = json.load(open('./stations_formatted_updated.json', 'r', encoding='utf-8'))


def verify_connections(data):
    dataset_errors = 1
    
    for station, details in data.items():
        
        if 'connections' in details:
            
            for line, line_details in details['connections'].items():
                for connection in line_details['connections']:
                    connected_station = list(connection.keys())[0]
                    
                    
                    if connected_station in data:
                        if line in data[connected_station]['connections']:
                            
                            reciprocal_connections = [list(conn.keys())[0] for conn in data[connected_station]['connections'][line]['connections']]
                            if station not in reciprocal_connections:
                                if (dataset_errors != 0):
                                    print(f"Missing reciprocal connection: {station} to {connected_station} on {line}")
                                dataset_errors += 1
                        else:
                            if (dataset_errors != 0):
                                print(f"{connected_station} does not list {line}")
                            dataset_errors += 1
                    else:
                        if (dataset_errors != 0):
                            print(f"{connected_station} is not in the dataset")
                        dataset_errors += 1
    print(f"Dataset errors: {dataset_errors}")
verify_connections(data)
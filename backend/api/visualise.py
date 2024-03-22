start_station = 'Brent Cross'
end_station = 'Finchley Road'

import json
import matplotlib.pyplot as plt
import networkx as nx
from mapping import searchRoute
from dataset import data, lines_data, reconstruct_path

def create_visualization_graph(data):
    G = nx.Graph()

    for station, details in data.items():
        # Swap the latitude and longitude if necessary to correctly represent your data
        G.add_node(station, pos=(details['longitude'], details['latitude']))  

        for connections in details['connections'].values():
            for connection in connections['connections']:
                for dest_station, dest_details in connection.items():
                    G.add_edge(station, dest_station, weight=dest_details['time'])

    return G

def visualize_graph(G, path, cost_so_far):
    plt.figure(figsize=(50, 50), dpi=150)  # Consider adjusting the figure size as needed
    
    pos = nx.get_node_attributes(G, 'pos')
    
    # Draw the graph with lightblue nodes and gray edges
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=8)
    
    # Highlight the path in blue and red
    path_stations = [station for station, _ in path]
    path_edges = [(path_stations[i], path_stations[i+1]) for i in range(len(path_stations)-1)]
    nx.draw_networkx_nodes(G, pos, nodelist=path_stations, node_color='blue', node_size=100)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    # Draw node labels
    for station, _ in path:
        x, y = pos[station]
        plt.text(x, y, s=station, bbox=dict(facecolor='red', alpha=0.5), horizontalalignment='center')

    # Draw cost labels
    for station, _ in path:
        x, y = pos[station]
        cost = cost_so_far[station]
        plt.text(x, y+0.001, s=f"Cost: {cost}", bbox=dict(facecolor='blue', alpha=0.5), horizontalalignment='center')

    plt.savefig('path_plot.png', dpi=150)  # Saves the plot to a file


# Running the search and visualization
came_from, cost_so_far, graph, _, current_line = searchRoute(data, lines_data, start_station, end_station)
path = reconstruct_path(came_from, current_line, start_station, end_station)

G = create_visualization_graph(data)
visualize_graph(G, path, cost_so_far)

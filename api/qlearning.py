from dataset import data
import random
import numpy as np

def qMapping(data):    
    graph_with_lines = {}

    for station, info in data.items():
        for line, line_info in info["connections"].items():
            for connection in line_info["connections"]:
                for target_station, travel_info in connection.items():
                    # The key for each connection now includes the line information
                    action = (target_station, line)  # Action is now a tuple of destination station and line
                    graph_with_lines.setdefault(station, {})[action] = -travel_info["time"]


                    
    return graph_with_lines

graph = qMapping(data)

alpha = 0.1
gamma = 0.6
epsilon = 0.1

Q_table = {}

#initialize Q_table with zeros
for station, actions in graph.items():
    for action in actions:
        Q_table[(station, action)] = 0

#similating the current state and available actions
current_state = 'Brent Cross'
available_actions = list(graph[current_state].keys())

#simulating the action selection
action = random.choice(available_actions)

next_state, line = action
reward = graph[current_state][action]

next_state_actions = graph.get(next_state, {})
max_future_q = max([Q_table.get((next_state, a), 0) for a in next_state_actions], default=0)
Q_table[(current_state, action)] = (1 - alpha) * Q_table[(current_state, action)] + alpha * (reward + gamma * max_future_q)

print(Q_table[(current_state, action)])

#simulating the action selection
# Number of episodes for training
num_episodes = 1000

# Maximum steps per episode to avoid infinite loops
max_steps_per_episode = 100

# Exploration-exploitation parameters
epsilon_start = 1.0
epsilon_end = 0.1
epsilon_decay = 0.001

# Initialize epsilon
epsilon = epsilon_start

for episode in range(num_episodes):
    state = random.choice(list(graph.keys()))  # Start from a random station
    for step in range(max_steps_per_episode):
        # Exploration-exploitation decision
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold < epsilon:
            action = random.choice(list(graph[state].keys()))  # Explore
        else:
            # Exploit the best known action
            action = max(graph[state], key=lambda x: Q_table.get((state, x), 0))
        
        # Take action, get next state and reward
        next_state, _ = action
        reward = graph[state][action]

        # Update Q-table
        next_max = max([Q_table.get((next_state, a), 0) for a in graph.get(next_state, {})], default=0)
        Q_table[(state, action)] = Q_table.get((state, action), 0) + alpha * (reward + gamma * next_max - Q_table.get((state, action), 0))

        # Update state
        state = next_state

        # Reduce epsilon
        epsilon = epsilon_end + (epsilon_start - epsilon_end) * np.exp(-epsilon_decay * episode)

    # Optional: Check for convergence or improvement here



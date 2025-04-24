import pickle
import numpy as np
import json
from crop_env import CropRotationEnv

# Load the trained Q-table
with open('output/trained_q_table.pkl', 'rb') as f:
    trained_q_table = pickle.load(f)

# Load crop data
with open('crop_data.json') as f:
    crop_data = json.load(f)

# Initialize the environment
env = CropRotationEnv(crop_data)

# Print some info about the Q-table
print(f"Number of state-action pairs in Q-table: {len(trained_q_table)}")
print("Sample of Q-table entries:")
sample_count = 0
for (state, action), value in list(trained_q_table.items())[:5]:
    print(f"State: {state}, Action: {action}, Q-value: {value}")
    sample_count += 1
    if sample_count >= 5:
        break

# Function to get the best action for a given state
def get_best_action(state):
    state_tuple = tuple(state)  # Ensure state is a tuple
    q_values = [trained_q_table.get((state_tuple, action), 0.0) for action in range(env.action_space.n)]
    return np.argmax(q_values)

# Test the agent
def test_agent(episodes=5, max_steps=10):
    rewards = []
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        print(f"\nEpisode {episode + 1}:")

        for step in range(max_steps):
            # Get best action
            action = get_best_action(state)
            next_state, reward, done, _ = env.step(action)
            
            print(f"Step {step + 1}:")
            print(f"State: {state}, Action: {action}, Reward: {reward}")
            state = next_state
            total_reward += reward
            
            if done:
                break

        rewards.append(total_reward)
        print(f"Total reward for episode {episode + 1}: {total_reward}")
    
    avg_reward = np.mean(rewards)
    print(f"\nAverage reward after {episodes} episodes: {avg_reward}")

# Print Q-values for a specific state - use actual states from your environment
def print_q_values_for_state(state):
    state_tuple = tuple(state)
    print(f"\nQ-values for state {state_tuple}:")
    q_values = [trained_q_table.get((state_tuple, action), 0.0) for action in range(env.action_space.n)]
    
    # Find the best action
    best_action = np.argmax(q_values)
    
    for action, q_value in enumerate(q_values):
        best_marker = " (BEST)" if action == best_action else ""
        print(f"Action {action}: Q-value = {q_value}{best_marker}")

# Test the agent
test_agent()

# Get some actual visited states from the Q-table
visited_states = list(set(state for (state, _) in trained_q_table.keys()))
print(f"\nTotal unique states visited during training: {len(visited_states)}")

# Print Q-values for a few actually visited states
for i, state in enumerate(visited_states[:3]):
    print_q_values_for_state(state)
    if i >= 2:  # Limit to 3 states
        break
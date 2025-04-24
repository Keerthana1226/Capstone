import json
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from crop_env import CropRotationEnv  # Make sure crop_env.py is in the same directory or properly imported

# Load crop data from JSON file
with open('crop_data.json') as f:
    crop_data = json.load(f)

# Initialize the environment
env = CropRotationEnv(crop_data)

# Hyperparameters
episodes = 5000
alpha = 0.1       # Learning rate
gamma = 0.9       # Discount factor
epsilon = 1.0     # Initial exploration rate
epsilon_decay = 0.997
min_epsilon = 0.01
max_steps = 15    # Max steps per episode

# Q-table as a dictionary
Q_table = {}
visit_counts = defaultdict(int)
reward_history = []

def get_q(state, action):
    return Q_table.get((tuple(state), action), 0.0)

# Training loop
for episode in range(episodes):
    state = env.reset()
    total_reward = 0

    for step in range(max_steps):
        # Choose action using epsilon-greedy policy
        if np.random.rand() < epsilon:
            action = env.action_space.sample()
        else:
            q_vals = [get_q(state, a) for a in range(env.action_space.n)]
            action = int(np.argmax(q_vals))

        next_state, reward, done, info = env.step(action)

        # Update Q-table
        current_q = get_q(state, action)
        best_next_q = max([get_q(next_state, a) for a in range(env.action_space.n)])
        Q_table[(tuple(state), action)] = current_q + alpha * (reward + gamma * best_next_q - current_q)

        # Update state visit count and reward
        visit_counts[tuple(state)] += 1
        total_reward += reward
        state = next_state

        if done:
            break

    reward_history.append(total_reward)

    # Decay epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

    if (episode + 1) % 100 == 0:
        print(f"Episode {episode+1} - Total Reward: {total_reward:.2f} - Epsilon: {epsilon:.3f}")

# Ensure the output directory exists
os.makedirs('output', exist_ok=True)

# Save Q-table to file
with open('output/trained_q_table.pkl', 'wb') as f:
    pickle.dump(Q_table, f)

# Save visit counts (optional)
with open('output/state_visit_counts.pkl', 'wb') as f:
    pickle.dump(dict(visit_counts), f)

# Plotting total rewards per episode
# plt.plot(reward_history)
# plt.xlabel("Episode")
# plt.ylabel("Total Reward")
# plt.title("Reward per Episode during Q-Learning")
# plt.grid(True)
# plt.savefig("output/reward_plot.png")
# plt.show()

print("✅ Training complete. Q-table saved to 'output/trained_q_table.pkl'")
print("📊 Reward plot saved to 'output/reward_plot.png'")
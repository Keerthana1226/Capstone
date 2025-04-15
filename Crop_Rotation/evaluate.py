from stable_baselines3 import PPO
from env.crop_rotation_env import CropRotationEnv

model = PPO.load("models/ppo_crop_rotation")
env = CropRotationEnv('dataset/indian_crop_dataset.json')

obs, _ = env.reset()
done = False
total_reward = 0

while not done:
    action, _ = model.predict(obs)
    obs, reward, done, _, _ = env.step(action)
    env.render()
    total_reward += reward

print(f"Total Reward: {total_reward}")

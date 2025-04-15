from stable_baselines3 import PPO
from env.crop_rotation_env import CropRotationEnv
from stable_baselines3.common.env_util import DummyVecEnv
import os

env = lambda: CropRotationEnv('dataset/indian_crop_dataset.json')
vec_env = DummyVecEnv([env])

model = PPO("MlpPolicy", vec_env, verbose=1)
model.learn(total_timesteps=50000)

os.makedirs("models", exist_ok=True)
model.save("models/ppo_crop_rotation")

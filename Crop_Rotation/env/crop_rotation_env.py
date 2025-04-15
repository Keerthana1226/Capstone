import gymnasium as gym
from gymnasium import spaces
import numpy as np
import json

class CropRotationEnv(gym.Env):
    def __init__(self, dataset_path, total_months=24):
        super(CropRotationEnv, self).__init__()
        with open(dataset_path, 'r') as f:
            self.crops = json.load(f)

        self.crop_list = list(self.crops.keys())
        self.total_months = total_months

        self.action_space = spaces.Discrete(len(self.crop_list))
        self.observation_space = spaces.Discrete(self.total_months)
        self.reset()

    def reset(self, seed=None, options=None):
        self.current_month = 1
        self.previous_crop = None
        return self.current_month, {}

    def step(self, action):
        selected_crop = self.crop_list[action]
        crop_info = self.crops[selected_crop]

        planting_start, planting_end = crop_info['planting_months']
        growth_duration = crop_info['grow_duration']
        reward = 0

        if planting_start <= self.current_month <= planting_end:
            reward += 1
            if self.previous_crop in crop_info['successor_crops']:
                reward += 1
        else:
            reward -= 1

        self.previous_crop = selected_crop
        self.current_month = (self.current_month + growth_duration) % self.total_months
        done = self.current_month == 0

        return self.current_month, reward, done, False, {}

    def render(self):
        print(f"Month: {self.current_month}, Last Crop: {self.previous_crop}")

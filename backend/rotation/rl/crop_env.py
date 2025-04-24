import gym
import json
import numpy as np
from gym import spaces

class CropRotationEnv(gym.Env):
    def __init__(self, crop_data, start_month=None, max_steps=24):
        super(CropRotationEnv, self).__init__()
        self.crop_data = crop_data
        self.crop_list = list(crop_data.keys())
        self.crop_to_idx = {crop: idx for idx, crop in enumerate(self.crop_list)}
        self.idx_to_crop = {idx: crop for crop, idx in self.crop_to_idx.items()}

        self.num_crops = len(self.crop_list)
        self.start_month = start_month  # Can be None to allow random initialization
        self.max_steps = max_steps

        # Month (1-12), crop idx (+1 for None)
        self.observation_space = spaces.MultiDiscrete([12, self.num_crops + 1])
        self.action_space = spaces.Discrete(self.num_crops)

        self.reset()

    def reset(self):
        # If no start month specified or if we want to randomize for better coverage
        if self.start_month is None:
            self.month = np.random.randint(1, 13)  # Random month from 1-12
        else:
            self.month = self.start_month
        
        self.current_crop = None
        self.prev_crop = None
        self.steps = 0
        return self._get_obs()

    def _get_obs(self):
        crop_idx = self.crop_to_idx[self.current_crop] if self.current_crop else self.num_crops
        return np.array([self.month, crop_idx])

    def _advance_time(self, duration):
        self.month += duration
        if self.month > 12:
            self.month = self.month % 12 or 12

    def get_season(self, month):
        if month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        elif month in [9, 10, 11]:
            return "Fall"
        else:  # 12, 1, 2
            return "Winter"

    def step(self, action):
        selected_crop = self.idx_to_crop[action]
        crop_info = self.crop_data[selected_crop]

        reward = 0
        done = False
        info = {
            "selected_crop": selected_crop,
            "current_month": self.month,
            "season": self.get_season(self.month)
        }

        # Check if this is a good planting month
        if self.month not in crop_info.get("planting_months", []):
            reward -= 5
            info["wrong_planting_month"] = True
        else:
            # Check crop rotation compatibility
            if self.prev_crop:
                successor_crops = self.crop_data[self.prev_crop].get("successor_crops", [])
                if selected_crop not in successor_crops:
                    reward -= 2
                    info["poor_succession"] = True
                
                # Avoid planting from same family
                if self.crop_data[selected_crop].get("family") == self.crop_data[self.prev_crop].get("family"):
                    reward -= 1
                    info["same_family"] = True
            
            # Base reward for suitable crop
            reward += 10
            
            # Update crop history
            self.prev_crop = self.current_crop
            self.current_crop = selected_crop
            
            # Update time based on crop grow duration
            grow_duration = crop_info.get("grow_duration", 1)
            self._advance_time(grow_duration)

        self.steps += 1
        if self.steps >= self.max_steps:
            done = True

        return self._get_obs(), reward, done, info

    def set_month(self, month):
        """Allow setting the month directly for exploration purposes"""
        if 1 <= month <= 12:
            self.month = month
        else:
            raise ValueError("Month must be between 1 and 12")
        return self._get_obs()
    
    def set_crop(self, crop_name):
        """Allow setting the current crop directly for exploration purposes"""
        if crop_name in self.crop_list:
            self.current_crop = crop_name
        elif crop_name is None:
            self.current_crop = None
        else:
            raise ValueError(f"Unknown crop: {crop_name}")
        return self._get_obs()
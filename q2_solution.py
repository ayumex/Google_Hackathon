import numpy as np
from stable_baselines3 import DDPG
from stable_baselines3.common.env_util import make_vec_env

from gym import Env
from gym.spaces import Box

class NOCEnvironment(Env):
    def __init__(self):
        super(NOCEnvironment, self).__init__()
        self.action_space = Box(low=-1, high=1, shape=(4,), dtype=np.float32)
        self.observation_space = Box(low=0, high=1, shape=(4,), dtype=np.float32)
        self.buffer_occupancy = 0.5  # Initial buffer occupancy
        self.arbitration_rate_cpu = 0.6  # Initial arbitration rate for CPU
        self.arbitration_rate_io = 0.4   # Initial arbitration rate for IO
        self.power_consumption = 0.7  # Initial power consumption

    def step(self, action):
        # Update NOC parameters based on the chosen action
        self.buffer_occupancy += action[0]
        self.arbitration_rate_cpu += action[1]
        self.arbitration_rate_io += action[2]
        self.power_consumption += action[3]

        # Calculate reward based on NOC performance metrics
        reward = self.calculate_reward()

        # Observe new state after taking action
        new_state = [self.buffer_occupancy, self.arbitration_rate_cpu, self.arbitration_rate_io, self.power_consumption]

        return np.array(new_state), reward, False, {}  # Return additional info as needed

    def reset(self):
        # Reset the environment
        self.buffer_occupancy = 0.5
        self.arbitration_rate_cpu = 0.6
        self.arbitration_rate_io = 0.4
        self.power_consumption = 0.7
        return np.array([self.buffer_occupancy, self.arbitration_rate_cpu, self.arbitration_rate_io, self.power_consumption])

    def seed(self, seed=None):
        pass  # No need to implement any functionality for seed method

    def calculate_reward(self):
        # Example reward function: maximize bandwidth and minimize latency while optimizing power efficiency
        reward = 0.5 * (1 - self.buffer_occupancy) + 0.3 * (self.arbitration_rate_cpu + self.arbitration_rate_io) + 0.2 * (1 - self.power_consumption)
        return reward

# Create and wrap the NOC environment
env = make_vec_env(lambda: NOCEnvironment(), n_envs=1)

# Define and train the DDPG agent
model = DDPG("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Save the trained model
model.save("ddpg_noc_model")

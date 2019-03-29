import hexafunc as simulator
import LoadAndUnLoadObservation as lu
from EnvironmentSetup import Environment
import numpy as np
from DQN_Core import DQN

def train(agent, env):    
    for epoch in range(5000):
        state = env.reset_environment()
        total_reward = 0
        
        file = open("epsilon.txt", 'r')
        epsilon = file.readline()
        epsilon = float(epsilon)
        agent.epsilon = epsilon

        for t in range(agent.batch_size):
            action = agent.get_action(state)
            reward, state_next, terminal = env.step(action)      # need to modify the step function
            action = env.action_number(action)      # get action index e.g. Leg_1_3_5_up = 1
            agent.remember(state, action, reward, state_next, terminal)
            state = state_next
            total_reward += reward

        agent.experiance_replay()
        lu.save_weights(agent)

        print("Total reward after ", epoch," epoch is:",total_reward)

if __name__ == '__main__':
    simulator.startConnection('127.0.0.1',19997)
    env  =  Environment("DQN")
    agent = DQN(64, 6, 0.1, 0.9)
    lu.load_weights(agent)
    train(agent, env)

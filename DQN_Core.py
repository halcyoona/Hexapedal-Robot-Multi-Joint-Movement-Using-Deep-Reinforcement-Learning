# all keras code goes here
#import keras
from EnvironmentSetup import Environment
from keras.layers import Conv2D, Dense, Flatten, InputLayer
from collections import deque 
from keras.utils import np_utils
import numpy as np
import random
import keras

class DQN:
    def __init__(self, state_shape, total_action, epsilon, gamma):

        self.batch_size = 30
        self.state_shape = state_shape
        self.total_action = total_action
        self.memory = deque(maxlen = 200000)
        self.epsilon = epsilon
        self.gamma = gamma
        self.env = Environment()
        self.network = keras.models.Sequential()

        self.network.add(Conv2D(16, (3, 3), strides=2, activation='relu', input_shape=(64, 64, 1)))
        self.network.add(Conv2D(32, (3, 3), strides=2, activation='relu'))
        self.network.add(Conv2D(64, (3, 3), strides=2, activation='relu'))
        self.network.add(Flatten())
        self.network.add(Dense(256, activation='relu'))
        self.network.add(Dense(6, activation='linear'))
        self.optimizer = keras.optimizers.RMSprop(lr=0.00025, rho=0.95, epsilon=0.01)
        self.network.compile(self.optimizer, loss='mse')

    #state, action, reward, state_next, terminal
    def remember(self, current_state, action, reward, next_state, done):
        self.memory.append((current_state, action, reward, next_state, done))
        
    
    def experiance_replay(self):
        #replay experiance
        batch = random.sample(self.memory, self.batch_size)

        for state, action, reward, next_state, done in batch:
            q_update = reward
            if not done:
                q_update = (reward + self.gamma * np.amax(self.network.predict(next_state)[0]))
            q_values = self.network.predict(state)
            q_values[0][action] = q_update
            self.network.fit(state, q_values, verbose=0)

    def get_action(self, state):
        possible_actions = self.env.action_list
        exploration = random.random()
        epsilon = self.epsilon
        chosen_action = ""
        if exploration <= epsilon:
            chosen_action = np.random.choice(possible_actions)
            #print("Action is: ", chosen_action)
        else:
            #print(self.network.predict(state))
            chosen_action = np.argmax(self.network.predict(state)[0])
            chosen_action = possible_actions[chosen_action]
            print("Action predicted: ", chosen_action)
        return chosen_action



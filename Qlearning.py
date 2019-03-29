from collections import defaultdict
import random, math
import numpy as np
import hexafunc as hexf
from EnvironmentSetup import Environment

class QLearningAgent:
    def __init__(self, alpha, epsilon, discount):
       
        self.conf = Environment()
        self.get_legal_actions = self.conf.get_action_list()     #get_legal_actions
        #automatically create new value for state and action if not found in the dictionary
        self._qvalues = defaultdict(lambda: defaultdict(lambda: 0))
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount

    def get_qvalues_table(self):
        """Returns _qvalues table"""
        return self._qvalues
        
    def get_qvalue(self, state, action):
        """ Returns Q(state,action) """
        return self._qvalues[state][action]

    def set_qvalue(self,state,action,value):
        """ Sets the Qvalue for [state,action] to the given value """
        self._qvalues[state][action] = value


    def get_value(self, state):
        """
        Compute your agent's estimate of V(s) using current q-values
        V(s) = max_over_action Q(state,action) over possible actions.
        Note: please take into account that q-values can be negative.
        """

        # need to modify the state code
       # pattern 1_leg_1_5_3_up
        state_action = state.split('_')
        leg = state_action[1]+state_action[2]+state_action[3]+state_action[4]
        _state = leg +'_'+ state_action[5]
    
        # now get legal action for that state
        #possible_actions = self.conf.get_legal_action(_state)
        possible_actions = self.conf.action_list
        #If there are no legal actions, return 0.0
        if len(possible_actions) == 0:
            return 0.0

        # setting the q-value
        q_values = []
        for i in range(len(possible_actions)):
            q_values.append(self.get_qvalue(state, possible_actions[i]))

        value = max(q_values)
        return value

    def update(self, state, action, reward, next_state):
        """
        You should do your Q-Value update here:
           Q(s,a) := (1 - alpha) * Q(s,a) + alpha * (r + gamma * V(s'))
        """

        #agent parameters
        gamma = self.discount
        learning_rate = self.alpha
        next_state = state
    
        q_value = (1-learning_rate)*self._qvalues[state][action]+learning_rate*(reward+gamma*self.get_value(next_state))
        
        self.set_qvalue(state, action, q_value)

    
    def get_best_action(self, state):
        """
        Compute the best action to take in a state (using current q-values). 
        """
        #need to modify the state code
        # pattern 1_leg_1_5_3_up
        state_action = state.split('_')
        leg = state_action[1]+state_action[2]+state_action[3]+state_action[4]
        _state = leg +'_'+ state_action[5]
        
        # now get legal action for that state
        #possible_actions = self.conf.get_legal_action(_state)
        #print("possible action are ", possible_actions)
        possible_actions = self.conf.action_list
        #If there are no legal actions, return None
        if len(possible_actions) == 0:
            return None
        
        max_value = self._qvalues[state][possible_actions[0]]
        stor_action = possible_actions[0]
        
        for i in possible_actions:
            val = self._qvalues[state][i]
            if(max_value<val):
                max_value = val
                stor_action = i
                
        best_action = stor_action
        # need to edit the code as Action is in the forn of 1_Leg_up
        return best_action

    def get_action(self, state):
        """
        Compute the action to take in the current state, including exploration.  
        With probability self.epsilon, we should take a random action.
            otherwise - the best policy action (self.getPolicy).
        
        Note: To pick randomly from a list, use random.choice(list). 
              To pick True or False with a given probablity, generate uniform number in [0, 1]
              and compare it with your probability
        """

        # Pick Action
        #need to modify the state code
        # pattern 1_leg_1_5_3_up
        state_action = state.split('_')
        leg = state_action[1]+state_action[2]+state_action[3]+state_action[4]
        _state = leg +'_'+ state_action[5]
    
   
        possible_actions = self.conf.action_list
        
        if len(possible_actions) == 0:
            return None

        #agent parameters:
        epsilon = self.epsilon
        exploration = random.random()
        #print("Exploration is: ",exploration)
        if exploration <= epsilon:
            chosen_action = np.random.choice(possible_actions)
            #print("Action is: ", chosen_action)
        else:
            chosen_action = self.get_best_action(state)
            print("choosen Action is ",chosen_action)
        
        return chosen_action # leg_6_2_4_up
        
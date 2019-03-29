#import tensorflow
from EnvironmentSetup import Environment
from Qlearning import QLearningAgent
import hexafunc as simulator
import LoadAndUnLoadObservation as lu

# current_state,next_state,reward,epsilon,decay_rate,Q_value:state

def train(env, agent):
    for i in range(5000):
        s = env.reset_environment()
        com_rewa = 0
        file = open("epsilon.txt", 'r')
        epsilon = file.readline()
        epsilon = float(epsilon)
        agent.epsilon = epsilon

        for t in range(90):
            
            info = ''
            q_states = ''
            prev = s    # previous state
            a = agent.get_action(s) # leg1_up
            print(a)
            r, next_s, _ = env.step(a)
            agent.update(s, a, r, next_s)
            s = next_s
            com_rewa += r

            Q_table = agent.get_qvalues_table()
            for key, values in Q_table[prev].items():
                q_states += key + '[' + str(values)+']'+','
            info += s+','+next_s+','+str(r)+','+str(agent.epsilon)+','+str(agent.discount)+','+str(com_rewa)+',' + q_states
            
            with open("log.txt",'a') as log:
                log.write(info+'\n')

        print("After ",i," iteration reward is:: ", com_rewa)
        lu.save_experiance(agent)
        lu.load_reward(i, com_rewa)
        env.reset_environment()


if __name__ == '__main__':
    simulator.startConnection('127.0.0.1',19997)
    env  =  Environment("Q-learning")
    agent = QLearningAgent(0.5, 0.9, 0.5)
    print("Loading the Agent experiances")
    lu.load_experiance(agent)
    train(env, agent)








import os

def load_reward(sim, rew):
    with open("Reward.txt", 'a') as file_handle:
        file_handle.write(str(sim) + "," + str(rew)+'\n')
    
def load_experiance(agent):
    '''
    load last-save q-values
    '''
    #if os.stat("Q-values.txt").st_size==0:
     #   print("Non-empty")
      #  return
    with open("Q-values.txt", 'r') as file:
        for line in file:
            state, action, value = line.strip().split(',')
            value = float(value)
            agent.set_qvalue(state, action, value)
        
def save_experiance(agent):
    '''
    storing hourly  Q-values 
    receive Q-agent
    save data in file
    '''
   
    Q_table = agent.get_qvalues_table()
    state_file = open("state_values.txt", 'w')
    with open("Q-values.txt", 'w') as file_handle:

        for s, a in Q_table.items():
            key, value = max(Q_table[s].items(), key=lambda x:x[1])
            state_file.write(s + "--->" +  str(value) + '\n')
            
            for _a, v in a.items():
                jvalue = s + ',' + _a + ',' + str(v) + '\n'
                file_handle.write(jvalue)

def maintain_log(agent, current_state, next_state, r, com_rewa):
    '''
    keep log of each state with detail information
    s,s',r,toal_r,Q(s)[0]
    '''
    Q_table = agent.get_qvalues_table()
    info = ''
    q_states = ''
    for key, values in Q_table[current_state].items():
        q_states += key + '[' + str(values)+']'+','
    info += current_state + ',' + next_state + ',' + str(r) + ',' + str(agent.epsilon) + ',' + str(agent.discount) + ',' + str(com_rewa) + ',' + q_states
            
    with open("log.txt",'a') as log:
        log.write(info+'\n')
        
def save_weights(agent):
    agent.network.save_weights("weights.h5")

def load_weights(agent):
    agent.network.load_weights("weights.h5")
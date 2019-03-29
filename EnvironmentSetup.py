import re
#import time
import hexafunc as hexf

class Environment:
    def __init__(self, method = "Q-learning"):
        self.stateNumb = 0
        self.lastaction = None
        self.state = None
        self.action_list=['Leg_1_5_3_up', 'Leg_1_5_3_down', 'Leg_1_5_3_forw', 'Leg_6_2_4_up', 'Leg_6_2_4_down', 'Leg_6_2_4_forw']

        self.legJointAngles = {'Leg1':{'up':[-20,-10],'down':[10,10],'forw':-30},
                              'Leg5':{'up':[20,5],'down':[-5,-10],'forw':25},
                              'Leg3':{'up':[-25,-10],'down':[13,-6],'forw':-20},
                              'Leg6':{'up':[25,10],'down':[-10,-10],'forw':30},
                              'Leg2':{'up':[-20,-5],'down':[5, 10],'forw':-20},
                              'Leg4':{'up':[25,10],'down':[-13,5],'forw':10}}

        self.method = method
        self.robot_intial_location = 2.0279
        self.last_location = 2.0279
        self.target_location, _, _ = hexf.getObjectPos("require_target")
        self.initial_state = 0
        self.last_remaining_distance = 0

    def reset_cover_distance(self):
        self.last_remaining_distance = self.robot_intial_location -  self.target_location
        self.last_location = 2.0279

    def action_number(self, action):
        return self.action_list.index(action)

    def get_legal_action(self, leg):
        if leg == "Leg1" or leg == "Leg3" or leg == "Leg5":
            reg = re.compile("(Leg1)+|(Leg3)+|(Leg5)+")
            return list(filter(reg.match, self.action_list))
        else:
            reg = re.compile("(Leg2)+|(Leg6)+|(Leg4)+")
            return list(filter(reg.match, self.action_list))

    def get_action_list(self):
        return self.action_list

    def get_action_list_length(self):
        return len(self.action_list)

    def get_leg_angles(self):
        return self.legJointAngles

    def reward(self, action):
        '''
        calculate reward on given action
        '''
        xo, _ , zo = hexf.getObjectPos("Ant")
        #beta = hexf.getObjectOrientation("Ant")
        min_height = 0.0300
        min_dis_cover = 0.0200
        remaining_dist = abs(xo) - self.target_location
        reward = 0
        print("last Ditance:", self.last_remaining_distance)
        print("current Distance:", remaining_dist)
        print("cover Distance:",self.last_remaining_distance - remaining_dist)
        if zo < min_height:
            reward -= 30
        
        # to handle backward behaviour
        if (abs(xo) - self.robot_intial_location > min_dis_cover):
            if (self.last_location - abs(xo) < 0):
                if(abs(self.last_location - abs(xo)) > min_dis_cover):
                    print("Backward reward -200 is Given:")
                    reward -= 200
            elif (self.last_location - abs(xo) > min_dis_cover and zo >= 0.0300 and zo <= 0.0700):
                print("Forward  reward of 200 is given:")
                reward += 200
            
        
        if (remaining_dist < self.last_remaining_distance and zo >= 0.0300 and zo <= 0.0700):
            if (self.last_remaining_distance - remaining_dist) >= min_dis_cover:
                self.last_remaining_distance = remaining_dist
                reward += 200
                print("Positive reward given is 200")
        
        if zo > 0.0750:
            reward -= 20

        reward -= 10
        self.last_location = abs(xo)
        return reward

    def reset_environment(self):
        ''' 
        Reset the whole environment e.g. position, states number
        return random action
        '''
        hexf.loadScene()
        hexf.resetPosition()
        self.reset_cover_distance()    # reset last episode cover distance
        if self.method == "Q-learning":
            self.stateNumb = 0
            self.initial_state = str(self.stateNumb) + '_' + 'Leg_1_5_3_up'
        else:
            self.initial_state = hexf.GetVisionSensorImage()
        
        return self.initial_state

    def perform_action(self, leg_handles, pos):
        '''
        perform multijoint movement e.g. moving three leg joint concurrently
        '''
        hexf.setMultijointPosition(leg_handles, pos)

    def prepare_joint_position(self, legName, legnum1, legnum2, legnum3, _action):

        handles = []
        pos = []
        _, legID = hexf.getJointLegID()
    
        if _action == "up":
            pos.append(self.legJointAngles[legName+str(legnum1)][_action][0])
            handles.append(legID[legnum1-1][1])
            pos.append(self.legJointAngles[legName+str(legnum2)][_action][0])
            handles.append(legID[legnum2-1][1])
            pos.append(self.legJointAngles[legName+str(legnum3)][_action][0])
            handles.append(legID[legnum3-1][1])
            pos.append(self.legJointAngles[legName+str(legnum1)][_action][1])
            handles.append(legID[legnum1-1][2])
            pos.append(self.legJointAngles[legName+str(legnum2)][_action][1])
            handles.append(legID[legnum2-1][2])
            pos.append(self.legJointAngles[legName+str(legnum3)][_action][1])
            handles.append(legID[legnum3-1][2])

        elif _action == "down":
            pos.append(self.legJointAngles[legName+str(legnum1)][_action][0])
            handles.append(legID[legnum1-1][1])
            pos.append(self.legJointAngles[legName+str(legnum2)][_action][0])
            handles.append(legID[legnum2-1][1])
            pos.append(self.legJointAngles[legName+str(legnum3)][_action][0])
            handles.append(legID[legnum3-1][1])
            pos.append(self.legJointAngles[legName+str(legnum1)][_action][1])
            handles.append(legID[legnum1-1][0])
            pos.append(self.legJointAngles[legName+str(legnum2)][_action][1])
            handles.append(legID[legnum2-1][0])
            pos.append(self.legJointAngles[legName+str(legnum3)][_action][1])
            handles.append(legID[legnum3-1][0])

            
        else:
            pos.append(self.legJointAngles[legName+str(legnum1)][_action])
            handles.append(legID[legnum1-1][0])
            pos.append(self.legJointAngles[legName+str(legnum2)][_action])
            handles.append(legID[legnum2-1][0])
            pos.append(self.legJointAngles[legName+str(legnum3)][_action])
            handles.append(legID[legnum3-1][0])

        return handles, pos


    def step(self, action):
        '''
        receive action as input.The action format is the following
        action = Leg_1_3_5_up
        pos: get position for each leg e.g leg1,3,5 on action up
        '''

        pos = []
        handles = []

        legName, legnum1, legnum2, legnum3, _action = action.split('_')
        legnum1 = int(legnum1)
        legnum2 = int(legnum2)
        legnum3 = int(legnum3)

        handles, pos = self.prepare_joint_position(legName, legnum1, legnum2, legnum3, _action)
        self.perform_action(handles, pos)
        r = self.reward(action)
        next_state = None
        if self.method == "Q-learning":
            self.state = self.stateNumb
            self.stateNumb += 1
            next_state = str(self.stateNumb) + '_' + action
        elif self.method == "DQN":
            # get new state
            next_state = hexf.GetVisionSensorImage()
        return r, next_state, 0    # 0 for temporary purpose mean didn't reach to final state

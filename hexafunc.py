import vrep
import math
import time
import cv2
import numpy as np
clientID = -1

def startConnection(ip, port):
    '''
    Start the connection to the client using the ip and the port.
    Will close all connections before starting.
    return clientID
    '''
    closeConnection()
    global clientID
    clientID = vrep.simxStart(ip,port,True,True,5000,5)
    if clientID > -1:
        print("Connection is started ")
    return clientID

def validConnection():
    '''
    Returns true if connection is established.
    Will fail if clientID is -1
    '''
    if(clientID > -1): return True
    else: return False

def closeConnection():
    '''
    Close all connection to the client.
    '''
    clientID = -1
    vrep.simxFinish(clientID)

def startSimulation():
    if(validConnection):
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

def getJointLegID():
    '''
    Get all joints ID from the hexapod.
    Returns retCode, jointLeg
    '''
    if not(validConnection()):
        return
    jointID = []
    retCode = []
    for legIndex in range(6):
        jointID.append([])
        retCode.append([])
        for jointIndex in range(3):
            jointName = "Ant_joint" + str(jointIndex+1) + "Leg" + str(legIndex+1)
            lj = vrep.simxGetObjectHandle(clientID, jointName, vrep.simx_opmode_oneshot_wait)
            jointID[legIndex].append(lj[1])
            retCode[legIndex].append(lj[0])
    return retCode,jointID

def getJointLegPos(jointLeg):
    '''
    Get all joint's position from the hexapod.
    Returns retCode, jointPos
    '''
    if not(validConnection()):
        return
    jointPos = []
    retCode = []
    for legIndex in range(6):
        jointPos.append([])
        retCode.append([])
        for jointIndex in range(3):
            lj = vrep.simxGetJointPosition(clientID, jointLeg[legIndex][jointIndex], vrep.simx_opmode_oneshot)
            jointPos[legIndex].append(lj[1])
            retCode[legIndex].append(lj[0])
    return retCode, jointPos

def getOneJointLegId(jointName):
        '''
        return the individual joint leg id
        
        '''
        ret, id = vrep.simxGetObjectHandle(clientID, jointName, vrep.simx_opmode_oneshot_wait)
        return id

def setJointAngle(joint, angle, mode=0):
    '''
    Set the angle of a particular joint in degrees.
    Angle will be automatically set between -90 and 90.
    mode = 0 for torque/force mode.
    mode = 1 for passive mode.
    '''
   # print("Angle is changed for Joint ",joint)
    if not(validConnection()):
        return
    if(angle > 90):
        angle = 90
    elif(angle < -90):
        angle = -90
    if(mode==1): vrep.simxSetJointPosition(clientID, joint, angle*math.pi/180, vrep.simx_opmode_oneshot)
    else: vrep.simxSetJointTargetPosition(clientID, joint, angle * math.pi/180, vrep.simx_opmode_oneshot)
    
    time.sleep(1.5)

def getJointAngle(joint):
    '''
    Get the angle of a particular joint in degrees.
    return angle
    '''
    if not(validConnection()):
        return 0
    return vrep.simxGetJointPosition(clientID, joint, vrep.simx_opmode_blocking)[1] * 180 / math.pi
    

def changeJointAngle(joint, delta = 1, mode = 0):
    '''
    Change the given joint's angle by +1 degree or by setting delta to an integer.
    mode = 0 for torque/force mode.
    mode = 1 for passive mode.
    Warning: Works really slow
    '''
    if(validConnection()):
        angle = vrep.simxGetJointPosition(clientID, joint, vrep.simx_opmode_blocking)[1] * 180 / math.pi
        if(mode==1): vrep.simxSetJointPosition(clientID, joint, (angle+delta)*math.pi/180, vrep.simx_opmode_oneshot)
        else: vrep.simxSetJointTargetPosition(clientID, joint, (angle+delta)*math.pi/180, vrep.simx_opmode_oneshot)
    

def loadScene():
    '''
    Will close the scene and open the scene with the following filename.
    The file must be in the V-Rep Pro \"scenes\" folder.
    Do not add filetype.
    '''
    if validConnection():  
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        #vrep.simxCloseScene(clientID, vrep.simx_opmode_oneshot_wait)
        #vrep.simxLoadScene(clientID, "C:/new.ttt", False, vrep.simx_opmode_blocking)
        time.sleep(0.5)   # for confirmation that simulation is stop
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

def minmaxAngle(angle):
    if angle > 90: return 90
    elif angle < -90: return -90
    else: return angle

def dualPrint(msg):
    '''
    Print the following message to the current console window and V-Rep Pro console.
    '''
    if (validConnection()):    
        vrep.simxAddStatusbarMessage(clientID, msg, vrep.simx_opmode_oneshot_wait)
        print(msg)

def setStepMode(stepVelocity, stepAmplitude, stepHeight, movementDirection, rotationMode, movementStrength):
    if(validConnection()):
        vrep.simxSetFloatSignal(clientID, 'stepVelocity', stepVelocity, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetFloatSignal(clientID, 'stepVelocity', stepAmplitude, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetFloatSignal(clientID, 'stepHeight', stepHeight, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetFloatSignal(clientID, 'movementDirection', movementDirection, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetFloatSignal(clientID, 'rotationMode', rotationMode, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetFloatSignal(clientID, 'movementStrength', movementStrength, vrep.simx_opmode_oneshot_wait)

def pauseCommunication():
    '''
    Pause the socket communication temporay 
    '''
    if(validConnection()):
        vrep.simxPauseCommunication(clientID, vrep.simx_opmode_oneshot_wait)

def getObjectPos(object_name):
    '''
    Get x, y, z cordinates of desire object.
    '''
    ret, handle = vrep.simxGetObjectHandle(clientID, object_name, vrep.simx_opmode_blocking)
    ret, cord = vrep.simxGetObjectPosition(clientID,handle,-1,vrep.simx_opmode_blocking)
    return cord[0], cord[1], cord[2]

def resetPosition():
    '''
    Resetting robot position to desire predefine position
    x = -2.0280s
    y = -0.2250
    z = 0.0468
    '''
    emptyBuff = bytearray()
    vrep.simxCallScriptFunction(clientID,'Ant_bodyTextured',vrep.sim_scripttype_childscript,'resetting',[],[],[],emptyBuff,vrep.simx_opmode_oneshot_wait)

def getObjectOrientation(object):
    '''
    Get objectOrientation value e.g. alpha, beta, gamma
    values are in redian so we did some convertion e.g value/180/math.pi to convert it to angle
    '''
    handle = getOneJointLegId(object) # sorry for wrong convention
    ret, B = vrep.simxGetObjectOrientation(clientID, handle, -1, vrep.simx_opmode_blocking)
    beta = B[1]*180/math.pi
    
    return beta

def setMultijointPosition(joints, position):
        ''''
        Set multiple leg joint position at same time(paralled)
        '''
        # to convert int pos to float pos
        position = list(map(float, position))

        if len(joints) == 3:
            vrep.simxCallScriptFunction(clientID,'dummythread',vrep.sim_scripttype_childscript,'setAngles', joints, position, [], ' ', vrep.simx_opmode_oneshot_wait)
            time.sleep(0.5)
        else:   
             '''
             joints_123 = joints[0:3]
             joint_456 = joints[3:]
             pos_123 = position
             '''
             vrep.simxCallScriptFunction(clientID,'dummythread',vrep.sim_scripttype_childscript,'setAngles', joints[0:3], position[0:3], [], ' ', vrep.simx_opmode_oneshot_wait)
             time.sleep(0.5)
             vrep.simxCallScriptFunction(clientID,'dummythread',vrep.sim_scripttype_childscript,'setAngles', joints[3:], position[3:], [], ' ', vrep.simx_opmode_oneshot_wait)
             time.sleep(0.5)
        
def GetVisionSensorImage():

    res, v0 = vrep.simxGetObjectHandle(clientID,'Vision_sensor',vrep.simx_opmode_oneshot_wait)    
    res, resolution, image = vrep.simxGetVisionSensorImage(clientID,v0,0,vrep.simx_opmode_streaming)
    time.sleep(0.5)
    res, resolution, image = vrep.simxGetVisionSensorImage(clientID,v0,0,vrep.simx_opmode_buffer)
    # conversion to grayscale is undergo
    
    img = np.array(image, dtype = np.uint8)
    img.resize([resolution[0],resolution[1],3])
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img.reshape(1, 64, 64, 1)

    return img

                
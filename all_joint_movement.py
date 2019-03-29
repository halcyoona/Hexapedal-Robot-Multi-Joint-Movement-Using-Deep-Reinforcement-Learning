import vrep
import time
import hexafunc as hexa

clientID = -1
ip = '127.0.0.1'
port = 19997
clientID = hexa.startConnection(ip, port)

if hexa.validConnection():
    hexa.startSimulation()
    hexa.dualPrint("Connected to remote API server")

    jointLegRetCode, jointLeg = hexa.getJointLegID()
    jointPosRetCode, jointPos = hexa.getJointLegPos(jointLeg)
    
    hexa.dualPrint("Starting Movement")
    
    x = hexa.getJointAngle(jointLeg[1][0])
    inc = 1
    for i in range(360):
        for legIndex in range(6):
            for jointIndex in range(3):
                hexa.setJointAngle(jointLeg[legIndex][jointIndex], x)
        x = x + inc
        if(x >= 90 or x <= -90):
            x = inc * 90
            inc = inc * -1
        time.sleep(0.01)

    hexa.loadScene("basichexa.ttt")
    hexa.closeConnection()
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
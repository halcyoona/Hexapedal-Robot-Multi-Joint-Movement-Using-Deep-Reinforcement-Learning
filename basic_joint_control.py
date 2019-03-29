import vrep
import time
import hexafunc as hexa
import getchar

mainAngle = 100

clientID = -1
ip = '127.0.0.1'
port = 19997
clientID = hexa.startConnection(ip, port)
print("Attempting to Connect")

if hexa.validConnection():
    hexa.startSimulation()
    hexa.dualPrint("Connected to remote API server")

    # Data Initilatization

    jointLegRetCode, jointLeg = hexa.getJointLegID()
    jointPosRetCode, jointPos = hexa.getJointLegPos(jointLeg)

    jointAngle = [[0, 0, 0]] * 6

    for i in range(6):
        for j in range(3):
            jointAngle[i][j] = hexa.getJointAngle(jointLeg[i][j])

    time.sleep(1)

    hexa.dualPrint("Starting Movement")

    # Code starts here

    jointAngle = [[0, 0, 0]] * 6

    for i in range(6):
        for j in range(3):
            jointAngle[i][j] = hexa.getJointAngle(jointLeg[i][j])

    ch = '0'
    selectedJoint = 0
    selectedLeg = 0
    change = 'l'
    while(ch != 'q'):
        ch = getchar.getch()
        if(ch == 'l'):
            change = 'l'
            hexa.dualPrint("Leg Selection")
        elif(ch == 'j'):
            change = 'j'
            hexa.dualPrint("Joint Selection")
        elif(change == 'j' and ch >= '1' and ch <= '3'):
            selectedJoint = int(ch) - int('1')
            hexa.dualPrint("Leg: " + str(selectedLeg + 1) +
                           ", Joint: " + str(selectedJoint + 1))
        elif(change == 'l' and ch >= '1' and ch <= '6'):
            selectedLeg = int(ch) - int('1')
            hexa.dualPrint("Leg: " + str(selectedLeg + 1) +
                           ", Joint: " + str(selectedJoint + 1))
        elif(ch == 'w'):
            jointAngle[selectedLeg][selectedJoint] = hexa.minmaxAngle(
                jointAngle[selectedLeg][selectedJoint] + 1)
            hexa.setJointAngle(
                jointLeg[selectedLeg][selectedJoint], jointAngle[selectedLeg][selectedJoint])
        elif(ch == 's'):
            jointAngle[selectedLeg][selectedJoint] = hexa.minmaxAngle(
                jointAngle[selectedLeg][selectedJoint] - 1)
            hexa.setJointAngle(
                jointLeg[selectedLeg][selectedJoint], jointAngle[selectedLeg][selectedJoint])

    # Code ends here

    hexa.loadScene("basichexa.ttt")
    hexa.closeConnection()
else:
    print('Failed connecting to remote API server')
print('Program ended')

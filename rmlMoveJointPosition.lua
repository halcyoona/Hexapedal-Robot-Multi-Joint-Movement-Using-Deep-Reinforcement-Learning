setAngles = function(handle, pos, em, emp1)
    
    sim.setThreadAutomaticSwitch(false)
   
    maxVel= {0.01,0.01,0.01} -- rad/s
    maxAccel={0.001,0.001,0.001} -- rad/s^2
    maxJerk= {0.01,0.01,0.01} -- rad/s^3
    pos[1] = (pos[1]*3.14)/180
    pos[2] = (pos[2]*3.14)/180
    pos[3] = (pos[3]*3.14)/180
    
    local a,b,c,d,e
    a,b,c,d,e =sim.rmlMoveToJointPositions(handle,-1,nil,nil,maxVel, maxAccel,maxJerk,pos,nil,nil)
    
    sim.setThreadAutomaticSwitch(true)
    return {},{},{},''
end


    while sim.getSimulationState()~=sim.simulation_advancing_abouttostop do
    -- to save time..perform thread once in a simulation step t
    -- will start execution on t = t + dt
        sim.switchThread()
end

function sysCall_cleanup()
    -- Put some clean-up code here
end


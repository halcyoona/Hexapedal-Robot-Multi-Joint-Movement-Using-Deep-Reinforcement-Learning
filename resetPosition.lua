#Lua script for resetting the robot position

function resetting()
    local robotBaseHandle = sim.getObjectHandle("Ant")
    local robotObjects=sim.getObjectsInTree(robotBaseHandle,sim.handle_all,0)
    for i=1,#robotObjects,1 do
        sim.resetDynamicObject(robotObjects[i])
    end

-- Now you can move the robot to a new position
    local pos1 = {-2.0280,-0.2250,0.0468}
    sim.setObjectPosition(robotBaseHandle,-1,pos1)
end
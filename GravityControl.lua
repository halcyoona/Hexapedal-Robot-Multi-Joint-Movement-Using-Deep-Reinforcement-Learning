-- Add this to different shape as non threaded child script

function sysCall_init()
   shapeHandle=sim.getObjectHandle('Ant_body')
end

function sysCall_actuation()
    local gravityVect=sim.getArrayParameter(sim.arrayparam_gravity)
    local res,mass=sim.getObjectFloatParameter(shapeHandle,3005)
    local force={-gravityVect[1]*mass,-gravityVect[2]*mass,-gravityVect[3]*mass}
    sim.addForceAndTorque(shapeHandle,force,{0,0,0})
end
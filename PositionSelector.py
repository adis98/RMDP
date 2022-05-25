from VehicleRoute import VehicleRoute
import random

def positionSelector(vehicleLocation, vehicleRoute):
    len = 0
    currNode = vehicleRoute
    while currNode.next is not None:
        len += 1
        currNode = currNode.next
    return random.randint(1,max(len,1))

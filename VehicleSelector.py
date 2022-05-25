import random
from OrderGenerator import Order

def vehicleSelector(order, vehicleLocations, vehicleRoutes, numVehicles):
    return random.randint(0,numVehicles-1) #returns a number from 0 to numVehicles-1 to indicate which vehicle has been selected


# if __name__=="__main__":
#     print(vehicle_selector(2,3,60,80,10,[],[]))

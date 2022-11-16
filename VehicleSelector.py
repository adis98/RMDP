import numpy as np
from OrderGenerator import Order
from PositionSelector import positionSelector
from States import getPreDecisionState

def vehicleSelector(order, vehicleLocations, vehicleHops, numVehicles, currTime, mapSize, agent, strat):
    if strat == 'rnd':
        vehicle = np.random.randint(numVehicles)
        return vehicle, None
    elif strat == 'rl':
        pre_arrival_state = getPreDecisionState(vehicleLocations, vehicleHops, currTime, mapSize)
        order_deets = np.array([order.restaurantX, order.restaurantY, order.customerX, order.customerY, order.minDeliveryTime, order.maxDeliveryTime, order.capacity])
        pre_decision_state = np.concatenate((pre_arrival_state, order_deets))
        vehicle = agent.select_action(pre_decision_state)
        return vehicle, pre_decision_state
    elif strat == 'best1':
        bestV = None
        bestC = np.inf
        for vehicle in range(numVehicles):
            _, _, _, bestCost = positionSelector(vehicleLocations[vehicle], vehicleHops[vehicle],
                                                                             order.restaurantX, order.restaurantY,
                                                                             order.customerX, order.customerY, order,
                                                                             strat)
            if bestCost < bestC:
                bestV = vehicle

        return bestV, None


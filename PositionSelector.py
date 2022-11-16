import numpy as np

def positionSelector(vehicleLocation, vehicleRoute, resX, resY, cusX, cusY, order, strat):
    initialCost = calculateRouteCost(vehicleLocation, vehicleRoute)
    bestCost = np.inf
    bestrespos = None
    bestcuspos = None
    if strat == 'rnd':
        bestrespos = np.random.randint(len(vehicleRoute)+1)
        bestcuspos = np.random.randint(bestrespos+1, len(vehicleRoute)+2)
        return bestrespos, bestcuspos, initialCost, bestCost

    else:
        for respos in range(0, len(vehicleRoute)+1):
            for cuspos in range(respos+1, len(vehicleRoute)+2):
                vehicleRoute.insert(respos, [resX, resY, order])
                vehicleRoute.insert(cuspos, [cusX, cusY, order])
                cost = calculateRouteCost(vehicleLocation, vehicleRoute)
                if cost < bestCost:
                    bestcuspos = cuspos
                    bestrespos = respos
                    bestCost = cost
                del vehicleRoute[cuspos]  # to reset the route
                del vehicleRoute[respos]  # to reset the route
        return bestrespos, bestcuspos, initialCost, bestCost


def calculateRouteCost(vloc, vRoute):
    if len(vRoute) == 0:
        return 0
    else:
        curr = np.array(vloc)
        cost = 0
        for hop in vRoute:
            cost += np.sum(np.abs(curr - np.array(hop[:2])))
            curr = np.array(hop[:2])
        return cost

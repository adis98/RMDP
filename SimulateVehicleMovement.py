def singleVehicleStep(route, vLoc, curTime, mapSz, speed): #return the vehicle's updated route and its location
    newRoute, newvLoc = route, vLoc
    if(route.next is not None):
        order = route.next.order
        if(order.orderPickedUp == False):
            newRoute, newvLoc = pickUpOrderOrMoveToRestaurant(route, vLoc, curTime, mapSz, speed, order)
        elif(order.orderPickedUp == True and order.orderDelivered == False):
            newRoute, newvLoc = deliverOrder(newRoute, newvLoc, curTime, mapSz, speed, order)
    return newRoute, newvLoc

def pickUpOrderOrMoveToRestaurant(route, vLoc, curTime, mapSz, speed, order):
    targetX = order.restaurantX
    targetY = order.restaurantY
    vX = vLoc[0]
    vY = vLoc[1]
    speedLeft = speed
    if(vX != targetX):
        if(abs(targetX - vX) <= speed):
            vX = targetX
            speedLeft -= abs(targetX - vX)
        else:
            speedLeft = 0
            if(targetX < vX):
                vX -= speed
            else:
                vX += speed
    if(vY != targetY):
        if(abs(targetY - vY) <= speedLeft):
            vY = targetY
        else:
            if(targetY < vY):
                vY -= speedLeft
            else:
                vY += speedLeft
    if(vX == targetX and vY == targetY and curTime >= order.minDeliveryTime):
        order.orderPickedUp = True
    return route, [vX,vY]

def deliverOrder(route, vLoc, curTime, mapSz, speed, order):
    targetX = order.customerX
    targetY = order.customerY
    vX = vLoc[0]
    vY = vLoc[1]
    speedLeft = speed
    if(vX != targetX):
        if(abs(targetX - vX) <= speed):
            vX = targetX
            speedLeft -= abs(targetX - vX)
        else:
            speedLeft = 0
            if(targetX < vX):
                vX -= speed
            else:
                vX += speed
    if(vY != targetY):
        if(abs(targetY - vY) <= speedLeft):
            vY = targetY
        else:
            if(targetY < vY):
                vY -= speedLeft
            else:
                vY += speedLeft
    if(vX == targetX and vY == targetY and curTime >= order.minDeliveryTime):
        order.orderDelivered = True
        nextOrder = route.next.next
        route.next = nextOrder
        nextOrder.prev = route

    return route,[vX,vY]

import numpy as np


class Order:
    def __init__(self):
        self.customerX = 0
        self.customerY = 0
        self.restaurantX = 0
        self.restaurantY = 0
        self.maxDeliveryTime = 0
        self.minDeliveryTime = 0
        self.orderPlacedTime = 0
        self.orderPickedUp = False
        self.orderDelivered = False
        self.capacity = 0


def createOrder(mapSize, currentTime, minReadyTime, maxReadyTime,
                deliveryWindowTime, maxOrderCapacity):  # chooses the customer location and the restaurant number
    order = Order()
    order.customerX, order.customerY, order.restaurantX, order.restaurantY = np.random.randint(mapSize, size=4)
    order.maxDeliveryTime = currentTime + deliveryWindowTime
    order.minDeliveryTime = np.random.randint(minReadyTime, maxReadyTime + 1) + currentTime
    order.orderPlacedTime = currentTime
    order.orderDeliveryTime = None
    order.capacity = np.random.randint(1, maxOrderCapacity + 1)
    return order


def generateOrders(mapSize, numInitialOrders,
                   deliveryWindowTime, minOrderReadyTime, maxOrderReadyTime, maxOrderArrivalTime,
                   arrivalRate, maxOrderCapacity):
    orders = []
    for i in range(numInitialOrders):
        orders.append(
            createOrder(mapSize, 0, minOrderReadyTime, maxOrderReadyTime, deliveryWindowTime, maxOrderCapacity))
    for currTime in range(1, maxOrderArrivalTime):
        numOrders = np.random.poisson(arrivalRate)
        for j in range(numOrders):
            orders.append(
                createOrder(mapSize, currTime, minOrderReadyTime, maxOrderReadyTime, deliveryWindowTime,
                            maxOrderCapacity))
    return orders


def createDummyOrder():
    order = Order()
    return order

import numpy as np
import random
import time
import pickle

# mapSize = 100 #creates an N by N 2D grid
# simulationDuration = 400 #number of seconds to run the simulation for
# vehicleCrossTime = 20 #each vehicle takes crosstime steps to go from top to bottom or from left to right across the grid
# numInitialOrders = 60 #number of orders available at timestep 0
# deliveryWindowTime = 60
# minOrderReadyTime = 5 #min time it takes for an order to be prepared
# maxOrderReadyTime = 15
# maxOrderArrivalTime = 200 #upper bound on time after which new orders will not be accepted
# arrivalRate = 0.02 #the probability of an order arriving at any given time step


class Order():
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

    def createOrder(mapSize, currentTime, minReadyTime, maxReadyTime, deliveryWindowTime): #chooses the customer location and the restaurant number
            order = Order()
            order.customerX,order.customerY,order.restaurantX,order.restaurantY = np.random.randint(mapSize,size=4)
            order.maxDeliveryTime = currentTime+deliveryWindowTime
            order.minDeliveryTime = random.randint(minReadyTime, maxReadyTime+1) + currentTime
            order.orderPlacedTime = currentTime
            return order

    def generateOrders(self, mapSize = 100, simulationDuration = 400, vehicleCrossTime = 20, numInitialOrders = 60, deliveryWindowTime = 60, minOrderReadyTime = 5, maxOrderReadyTime = 15, maxOrderArrivalTime = 200, arrivalRate = 0.2):
        orders = []
        for i in range(numInitialOrders):
            orders.append(Order.createOrder(mapSize, 0, minOrderReadyTime, maxOrderReadyTime, deliveryWindowTime))
        for currTime in range(1,maxOrderArrivalTime):
            numOrders = np.random.poisson(arrivalRate)
            for j in range(numOrders):
                orders.append(Order.createOrder(mapSize, currTime, minOrderReadyTime, maxOrderReadyTime, deliveryWindowTime))
        return orders

        #print(numOrders)

            #order = createOrder(mapSize,i+deliveryWindowTime)
# if __name__=="__main__":
#     fileName = "orders.pkl"
#     orders = generateOrders() #returns a list of orders for the problem
#     with open(fileName, "wb") as f:
#         pickle.dump(orders, f)
#     with open(fileName, "rb") as f:
#         orders = pickle.load(f)
#         for order in orders:
#             print(order.customerX,order.customerY,order.minDeliveryTime,order.maxDeliveryTime)

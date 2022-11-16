from OrderGenerator import generateOrders, createDummyOrder
from VehicleSelector import vehicleSelector
from PositionSelector import positionSelector, calculateRouteCost
from SimulateVehicleMovement import singleVehicleStep
from Network import Agent
from States import getPreDecisionState, computeReward
import numpy as np
import torch
import csv

class Orchestrator:
    seed = None
    strategy = None
    numVehicles = 0
    mapSize = 0  # creates an N by N 2D grid
    simulationDuration = 0  # number of seconds to run the simulation for
    vehicleCrossTime = 0  # each vehicle takes crosstime steps to go from top to bottom or from left to right across the grid
    numInitialOrders = 0  # number of orders available at timestep 0
    deliveryWindowTime = 0
    minOrderReadyTime = 0  # min time it takes for an order to be prepared
    maxOrderReadyTime = 0
    maxOrderArrivalTime = 0  # upper bound on time after which new orders will not be accepted
    arrivalRate = 0  # the probability of an order arriving at any given time step
    vehicleLocations = []
    currentTime = 0
    maxOrderSize = 0  # the max storage space of an order
    vehicleMaxCap = 0  # The maximum order capacity a vehicle can carry. 20 means it can "cache" 4 orders if every order is size 5
    vehicleHops = []  # sequence of restaurant and customer hops
    orders = None
    agent = None
    writeFile = None
    @classmethod
    def setCommonVals(cls, numV=5, mSize=100, simDur=400, vCrossTime=20, numInitOrder=60, windowGap=60, minReadyTime=5,
                      maxReadyTime=15, maxOrderArrivalTime=200, arrivalRate=0.2, maxOrderSize=5, vehicleCap=20, seed=42, strategy='rl'):
        cls.numVehicles = numV
        cls.seed = seed
        cls.strategy = strategy
        np.random.seed(seed)
        torch.manual_seed(seed)
        cls.mapSize = mSize  # creates an N by N 2D grid
        cls.simulationDuration = simDur  # number of seconds to run the simulation for
        cls.vehicleCrossTime = vCrossTime  # each vehicle takes crosstime steps to go from top to bottom or from left to right across the grid
        cls.numInitialOrders = numInitOrder  # number of orders available at timestep 0
        cls.deliveryWindowTime = windowGap
        cls.minOrderReadyTime = minReadyTime  # min time it takes for an order to be prepared
        cls.maxOrderReadyTime = maxReadyTime
        cls.maxOrderArrivalTime = maxOrderArrivalTime  # upper bound on time after which new orders will not be accepted
        cls.arrivalRate = arrivalRate  # the probability of an order arriving at any given time step
        cls.vehicleLocations = []
        cls.currentTime = 0
        cls.maxOrderSize = maxOrderSize  # the max storage space of an order
        cls.vehicleMaxCap = vehicleCap  # The maximum order capacity a vehicle can carry. 20 means it can "cache" 4 orders if every order is size 5
        cls.vehicleHops = []  # sequence of restaurant and customer hops
        cls.agent = Agent()
        cls.writeFile1 = strategy+'_cost_vs_time.csv'
        # cls.writeFile2 = strategy+'_orders_vs_time.csv'
        for i in range(cls.numVehicles):
            cls.vehicleLocations.append([0, 0])
            cls.vehicleHops.append(
                [])  # each vehicle route is a list of restaurants and customer location hops. Follows constraint that order is picked up before delivery

    @classmethod
    def start(cls):
        cls.orders = generateOrders(cls.mapSize, cls.numInitialOrders, cls.deliveryWindowTime, cls.minOrderReadyTime,
                                    cls.maxOrderReadyTime, cls.maxOrderArrivalTime, cls.arrivalRate,
                                    cls.maxOrderSize)  # need to add params later

        f1 = open(cls.writeFile1, 'w')
        writer1 = csv.writer(f1)
        writer1.writerow(['time', 'total distance cost'])
        # f2 = open(cls.writeFile2, 'w')
        # writer2 = csv.writer(f2)
        # writer2.writerow(['time', 'orders in system'])
        while cls.currentTime < cls.simulationDuration:
            if cls.currentTime == 392:
                print()
            ordersForCurrentTimeStep = cls.getOrders(cls.currentTime)
            cls.vehicleHops = cls.scheduleOrders(ordersForCurrentTimeStep, cls.currentTime, cls.mapSize, cls.strategy)
            cls.currentTime, cls.vehicleLocations, cls.vehicleHops = cls.vehiclesStep(cls.numVehicles, cls.vehicleHops,
                                                                                      cls.vehicleLocations,
                                                                                      cls.currentTime, cls.mapSize,
                                                                                      cls.vehicleCrossTime)  # simulates movement of vehicles and updates, locations, routes, and time for one time step
            print("----time:", cls.currentTime)
            vehicleCosts = []
            # vehicleHopsLens = []
            for vehicle in range(cls.numVehicles):
                vehicleCosts.append(calculateRouteCost(cls.vehicleLocations[vehicle], cls.vehicleHops[vehicle]))
                # vehicleHopsLens.append(len(cls.vehicleHops[vehicle]))
            print(sum(vehicleCosts))
            writer1.writerow([cls.currentTime, sum(vehicleCosts)])
            # writer2.writerow([cls.currentTime, sum(vehicleHopsLens)])
        f1.close()
        # f2.close()
    @classmethod
    def getOrders(cls, currentTime):
        orders = []
        for order in cls.orders:
            if order.orderPlacedTime == currentTime:
                orders.append(order)
        return orders

    @classmethod
    def scheduleOrders(cls, orders, currTime, mapSize, strat):
        for order in orders:
            vehicleNum, pre_decision_state = vehicleSelector(order, cls.vehicleLocations,
                                                             cls.vehicleHops, cls.numVehicles, currTime,
                                                             mapSize, cls.agent, strat)

            bestrespos, bestcuspos, initialCost, bestCost = positionSelector(cls.vehicleLocations[vehicleNum],
                                                                             cls.vehicleHops[vehicleNum],
                                                                             order.restaurantX, order.restaurantY,
                                                                             order.customerX, order.customerY, order, strat)

            cls.vehicleHops[vehicleNum].insert(bestrespos, [order.restaurantX, order.restaurantY, order])
            cls.vehicleHops[vehicleNum].insert(bestcuspos, [order.customerX, order.customerY, order])
            if strat == 'rl':
                post_decision_state = getPreDecisionState(cls.vehicleLocations, cls.vehicleHops, currTime, mapSize)
                done = True if order == orders[-1] else False  # no more decisions if its the last order of the timestep
                reward = computeReward(initialCost, bestCost)
                next_order = orders[orders.index(order) + 1] if not done else createDummyOrder()
                next_order_deets = np.array(
                    [next_order.restaurantX, next_order.restaurantY, next_order.customerX, next_order.customerY,
                     next_order.minDeliveryTime, next_order.maxDeliveryTime, next_order.capacity])
                state_ = np.concatenate((post_decision_state, next_order_deets))
                cls.agent.store_transition(pre_decision_state, vehicleNum, reward, state_, done)
        return cls.vehicleHops

    @classmethod
    def vehiclesStep(cls, numV, routes, vLocs, curTime, mapSz, vCrossTime):
        for vehicle in range(numV):
            routes[vehicle], vLocs[vehicle] = singleVehicleStep(routes[vehicle], vLocs[vehicle], curTime, mapSz,
                                                                mapSz / vCrossTime)
        return curTime + 1, vLocs, routes

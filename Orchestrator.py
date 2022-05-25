from OrderGenerator import Order
from VehicleSelector import vehicleSelector
from PositionSelector import positionSelector
from VehicleRoute import VehicleRoute
from SimulateVehicleMovement import singleVehicleStep


class Orchestrator:
    def __init__(self, numV=5, mSize=100,simDur=400,vCrossTime=20,numInitOrder=60,windowGap=60,minReadyTime=5,maxReadyTime=15,maxOrderArrivalTime=200,arrivalRate=0.2):
        self.numVehicles=5
        self.mapSize = 100 #creates an N by N 2D grid
        self.simulationDuration = 400 #number of seconds to run the simulation for
        self.vehicleCrossTime = 20 #each vehicle takes crosstime steps to go from top to bottom or from left to right across the grid
        self.numInitialOrders = 60 #number of orders available at timestep 0
        self.deliveryWindowTime = 60
        self.minOrderReadyTime = 5 #min time it takes for an order to be prepared
        self.maxOrderReadyTime = 15
        self.maxOrderArrivalTime = 200 #upper bound on time after which new orders will not be accepted
        self.arrivalRate = 0.2 #the probability of an order arriving at any given time step
        self.vehicleLocations = []
        self.currentTime=0
        self.orders = None
        self.vehicleRoutes = []
        for i in range(self.numVehicles):
            self.vehicleLocations.append([0,0])
            self.vehicleRoutes.append(VehicleRoute())

    def start(self):
        generator = Order()
        self.orders = generator.generateOrders(self.mapSize, self.simulationDuration, self.vehicleCrossTime, self.numInitialOrders, self.deliveryWindowTime, self.minOrderReadyTime, self.maxOrderReadyTime, self.maxOrderArrivalTime, self.arrivalRate) #need to add params later
        while (self.currentTime < self.simulationDuration):
            ordersForCurrentTimeStep = self.getOrders(currentTime = self.currentTime)
            self.vehicleRoutes = self.scheduleOrders(ordersForCurrentTimeStep)
            self.currentTime, self.vehicleLocations, self.vehicleRoutes = self.vehiclesStep(self.numVehicles, self.vehicleRoutes, self.vehicleLocations, self.currentTime, self.mapSize, self.vehicleCrossTime) #simulates movement of vehicles and updates, locations, routes, and time for one time step
            print("----time:", self.currentTime)
            for vehicle in range(self.numVehicles):
                print("locn:", self.vehicleLocations[vehicle])


    def getOrders(self,currentTime):
        orders = []
        for order in self.orders:
            if(order.orderPlacedTime == currentTime):
                orders.append(order)
        return orders

    def scheduleOrders(self,orders):
        for order in orders:
            vehicleNum = vehicleSelector(order, self.vehicleLocations, self.vehicleRoutes, self.numVehicles)
            position = positionSelector(self.vehicleLocations[vehicleNum], self.vehicleRoutes[vehicleNum])
            self.vehicleRoutes[vehicleNum].insertOrder(order, position)
        return self.vehicleRoutes


    def vehiclesStep(self, numV, routes, vLocs, curTime, mapSz, vCrossTime):
        for vehicle in range(numV):
            routes[vehicle], vLocs[vehicle] = singleVehicleStep(routes[vehicle], vLocs[vehicle], curTime, mapSz, mapSz/vCrossTime)
        return curTime+1, vLocs, routes

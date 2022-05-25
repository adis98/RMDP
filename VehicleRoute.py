from OrderGenerator import Order

class VehicleRoute:
    def __init__(self, order= None):
        self.prev = None
        self.order = order
        self.next = None

    def insertOrder(self, order, position): #shift every order from this position and ahead by one step and place the new order here
        currNode = self
        currPos = 0
        newNode = VehicleRoute(order = order)

        while (currNode.next is not None and currPos != position):
            currNode = currNode.next
            currPos += 1

        if (currNode.next is None):
            currNode.next = newNode
            newNode.prev = currNode
        else:
            prevNode = currNode.prev
            nextNode = currNode.next
            prevNode.next = newNode
            newNode.prev = prevNode
            newNode.next = currNode
            currNode.prev = newNode

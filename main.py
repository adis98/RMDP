from Orchestrator import Orchestrator
import numpy as np
import csv

if __name__ == "__main__":
    Orchestrator.setCommonVals(numV=5, mSize=100, simDur=400, vCrossTime=20, numInitOrder=3, windowGap=60,
                               minReadyTime=5, maxReadyTime=15,
                               maxOrderArrivalTime=200, arrivalRate=0.2, maxOrderSize=5, vehicleCap=20, seed=42,
                               strategy='best1')
    Orchestrator.start()

    count = 0
    order_state = np.zeros(Orchestrator.simulationDuration + 1)
    writefile = Orchestrator.strategy + '_order_state_vs_time.csv'
    for order in Orchestrator.orders:
        order_state[order.orderPlacedTime:] += 1
        if order.orderDeliveryTime is not None:
            order_state[order.orderDeliveryTime:] -= 1
    f = open(writefile, 'w')
    writer = csv.writer(f)
    writer.writerow(['time', 'orders in system'])
    col1 = list(range(len(order_state)))
    col2 = order_state.tolist()
    combined = list(zip(col1, col2))
    writer.writerows(combined)
    f.close()

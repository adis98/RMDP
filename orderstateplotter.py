import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    for strat in ['rnd', 'rl', 'best1']:
        df = pd.read_csv("sample_experiments/"+strat+"_order_state_vs_time.csv")
        x = df['time'].values
        y = df['orders in system'].values
        plt.plot(x, y, label=strat)
    plt.xlabel('time step')
    plt.ylabel('active orders in the system')
    plt.legend()
    plt.title("Number of active orders in the system vs time steps")
    plt.savefig("sample_experiments/order_state_vs_time.png")
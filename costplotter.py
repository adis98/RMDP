import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    for strat in ['rnd', 'rl', 'best1']:
        df = pd.read_csv("sample_experiments/"+strat+"_cost_vs_time.csv")
        x = df['time'].values
        y = df['total distance cost'].values
        plt.plot(x, y, label=strat)
    plt.xlabel('time step')
    plt.ylabel('total distance cost')
    plt.legend()
    plt.title("Total distance cost vs time steps")
    plt.savefig("sample_experiments/cost_vs_time.png")
"""Pre built visualization tools

You are always welcome to BYO tools."""

import matplotlib.pyplot as plt

def plot_pyport_basic(solution_info:list, frontier_info:list, random_draw_info:list=[], *args, **kwargs):
    plt.figure(figsize=(8, 8))

    solution_returns      = solution_info[0]
    solution_volatilities = solution_info[1]
    plt.plot(solution_volatilities, solution_returns, 'r*', markersize=16.0)

    
    frontier_returns      = frontier_info[0]
    frontier_volatilities = frontier_info[1]
    plt.plot(frontier_volatilities, frontier_returns, 'g--')


    if random_draw_info:
        random_draw_returns      = random_draw_info[0]
        random_draw_volatilities = random_draw_info[1]
        plt.scatter(random_draw_volatilities, random_draw_returns, c=random_draw_returns/random_draw_volatilities, marker='o')

    plt.grid(True)
    plt.ylabel('Return')
    plt.xlabel('Volatility')
    plt.colorbar(label='Sharpe Ratio')
    plt.show(block=True)
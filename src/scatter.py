import os
import matplotlib.pyplot as plt
import numpy as np
def scatter_burn_rates():
    #all folders are within the main folder, named accordingly
    subsets = ['25h1, 25v1, 25h2, 25v2', '25h3', '25v3',
           '26h1, 26v1, 26h2, 26v2', '26h3', '26v3',
           '27h1, 27v1, 27h2, 27v2', '27h3', '27v3',
           '28h1, 28v1, 28h2, 28v2', '28h3', '28v3',]
    #12 colors, for 24 subfolders
    colors = 'maroon', 'red', 'salmon', 'darkgreen', 'limegreen', 'lime', 'mediumblue', 'royalblue', 'skyblue', 'indigo', 'blueviolet', 'violet'

    #going to just do this bit manually for now, just needs to be length 24
    burn_rates = np.linspace(1, 24, 24)
    #plotting with specimen on x-axis
    #need to have horiz and vert for each subset on one line

    data = {
        '25-1': (burn_rates[0], burn_rates[1]),
        '25-2': (burn_rates[2], burn_rates[3]),
        '25-3': (burn_rates[4], burn_rates[5]),
        '26-1': (burn_rates[6], burn_rates[7]),
        '26-2': (burn_rates[8], burn_rates[9]), 
        '26-3': (burn_rates[10], burn_rates[11]),
        '27-1': (burn_rates[12], burn_rates[13]),
        '27-2': (burn_rates[14], burn_rates[15]),
        '27-3': (burn_rates[16], burn_rates[17]),
        '28-1': (burn_rates[18], burn_rates[19]),
        '28-2': (burn_rates[20], burn_rates[21]),
        '28-3': (burn_rates[22], burn_rates[23]),
    }

    subsets = list(data.keys())
    x = np.arange(len(subsets))  # the label locations
    h_vals = [v[0] for v in data.values()]
    v_vals = [v[1] for v in data.values()]

    plt.figure(figsize=(12, 6))
    plt.scatter(x, h_vals, color='blue', label='Horizontal Burn', marker='o')
    plt.plot(x, h_vals, color='blue', linestyle='-', alpha=0.5)
    plt.scatter(x, v_vals, color='red', label='Vertical', marker='*')
    plt.plot(x, v_vals, color='red', linestyle='-', alpha=0.5)

    plt.xticks(x, subsets)
    plt.xlabel('Image Subset')
    plt.ylabel('Burn Rate')
    plt.title('Horizontal and Vertical Burn Rates for Images 25-28')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    #save the figure
    plt.savefig('burn_rates_scatter1.png')
    
    #plot the other way, with horizontal and vertical on axes
    plt.figure(figsize=(12, 6))
    
    #one color per subset
    for i, subset in enumerate(subsets):
        dataset_index = i//2
        color = colors[dataset_index % len(colors)]
        plt.scatter(h_vals[i], v_vals[i], color=color, marker='o')
        plt.scatter(v_vals[i], h_vals[i], color=color, marker='*')
    plt.xlabel('Horizontal Burn Rate')
    plt.ylabel('Vertical Burn Rate')
    plt.title('Horizontal vs Vertical Burn Rates for Images 25-28')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    #save the figure
    plt.savefig('burn_rates_scatter2.png')

while __name__ == '__main__':
    scatter_burn_rates()

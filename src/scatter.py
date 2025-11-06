import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
def scatter_burn_rates():
    #all folders are within the main folder, named accordingly
    subsets = ['1h1, 1v1, 1h2, 1v2', '1h3', '1v3',
           '2h1, 2v1, 2h2, 2v2', '2h3', '2v3',
           '3h1, 3v1, 3h2, 3v2', '3h3', '3v3',
           '4h1, 4v1, 4h2, 4v2', '4h3', '4v3',]
    #12 colors, for 24 subfolders
    colors = 'maroon', 'red', 'salmon', 'darkgreen', 'limegreen', 'lime', 'mediumblue', 'royalblue', 'skyblue', 'indigo', 'blueviolet', 'violet'

    #going to just do this bit manually for now, just needs to be length 24
    burn_rates = np.linspace(1, 24, 24)
    #plotting with specimen on x-axis
    #need to have horiz and vert for each subset on one line

    data = {
        '1-1': (burn_rates[0], burn_rates[1]),
        '1-2': (burn_rates[2], burn_rates[3]),
        '1-3': (burn_rates[4], burn_rates[5]),
        '2-1': (burn_rates[6], burn_rates[7]),
        '2-2': (burn_rates[8], burn_rates[9]), 
        '2-3': (burn_rates[10], burn_rates[11]),
        '3-1': (burn_rates[12], burn_rates[13]),
        '3-2': (burn_rates[14], burn_rates[15]),
        '3-3': (burn_rates[16], burn_rates[17]),
        '4-1': (burn_rates[18], burn_rates[19]),
        '4-2': (burn_rates[20], burn_rates[21]),
        '4-3': (burn_rates[22], burn_rates[23]),
    }

    subsets = list(data.keys())
    x = np.arange(len(subsets))  # the label locations
    h_vals = [v[0] for v in data.values()]
    v_vals = [v[1] for v in data.values()]

    plt.figure(figsize=(12, 6))
    plt.scatter(x, h_vals, color='blue', label='Horizontal Burn', marker='o')
    plt.scatter(x, v_vals, color='red', label='Vertical', marker='*')
    

    plt.xticks(x, subsets)
    plt.xlabel('Image Subset')
    plt.ylabel('Burn Rate')
    plt.title('Horizontal and Vertical Burn Rates for Images 1-4')
    plt.legend()
    plt.plot(x, h_vals, color='blue', linestyle='-', alpha=0.5)
    plt.plot(x, v_vals, color='red', linestyle='-', alpha=0.5)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    #save the figure
    plt.savefig('burn_rates_scatter1.png')
    
    #plot the other way, with horizontal and vertical on axes
    plt.figure(figsize=(12, 6))
    
    #one color per subset
    for i, subset in enumerate(subsets):
        subset_name = subsets[i]
        color = colors[i]
        plt.scatter(h_vals[i], v_vals[i], color=color, marker='o')
        plt.scatter(v_vals[i], h_vals[i], color=color, marker='*')
    plt.xlabel('Horizontal Burn Rate')
    plt.ylabel('Vertical Burn Rate')
    plt.title('Burn Rates: Horizontal vs Vertical Correlation')
    #make legend, 12 colors
    patches = []
    for i, subset in enumerate(subsets):
        color = colors[i]
        patch = mpatches.Patch(color=color, label=subset)
        patches.append(patch)
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    #save the figure
    plt.savefig('burn_rates_scatter2.png')

while __name__ == '__main__':
    scatter_burn_rates()

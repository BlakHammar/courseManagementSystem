import sys
import numpy as np
import matplotlib.pyplot as plt


def visualize(grid_file, output_image):
    grid = np.loadtxt(grid_file, delimiter=',')

    # Define temperature ranges and corresponding colors
    temperature_ranges = [-np.inf, 0, 10, 20, 30, 40, 50, 60, np.inf]
    colors = ['darkblue', 'blue', 'aqua', 'lawngreen', 'yellow', 'orange', 'red', 'darkred']

    # Create color map based on temperature ranges
    color_map = np.zeros(grid.shape, dtype='U10')
    for i in range(1, len(temperature_ranges)):
        color_map[(grid > temperature_ranges[i - 1]) & (grid <= temperature_ranges[i])] = colors[i - 1]

    # Create scatter plot
    fig, ax = plt.subplots()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            ax.scatter(j, grid.shape[0] - i - 1, color=color_map[i, j], s=50)

    ax.set_title('Temperature Distribution')
    ax.set_xlabel('Column')
    ax.set_ylabel('Row')
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.savefig(output_image)
    plt.show()


if __name__ == '__main__':
    grid_file = sys.argv[1]
    output_image = sys.argv[2]
    visualize(grid_file, output_image)



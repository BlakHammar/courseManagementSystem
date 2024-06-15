import numpy as np
import multiprocessing as mp

def calculateTemp(partition):
    newPartition = np.copy(partition)
    for i in range(1, partition.shape[0] - 1):
        for j in range(1, partition.shape[1] - 1):
            if partition[i, j] == 0:
                newPartition[i, j] = 0.25 * (partition[i - 1, j] + partition[i + 1, j] + partition[i, j - 1] + partition[i, j + 1])
    return newPartition

def updateGrid(grid, results, gridSize):
    for i, partition in enumerate(results):
        if 2 * i + 2 <= gridSize:
            grid[2 * i:2 * (i + 1), :] = partition[1:3, 1:-1]
        else:
            grid[2 * i:gridSize, :] = partition[1:2, 1:-1]
    return grid

if __name__ == '__main__':
    startTemp = int(input('Enter temperature in Celsius: '))
    gridSize = startTemp  # Use the starting temperature as the grid size

    arrWithoutHalo = np.zeros((gridSize, gridSize))
    prevArr = np.zeros((gridSize + 2, gridSize + 2))

    # Set the leftmost column after halo cells to startTemp
    prevArr[1:gridSize + 1, 1] = startTemp
    arrWithoutHalo[:, 0] = startTemp

    currArr = np.copy(prevArr)

    # Create a pool of processes
    pool = mp.Pool(mp.cpu_count())

    # Partition arrWithoutHalo by 2xN arrays, handling odd grid sizes
    partitions = []
    for i in range(0, gridSize, 2):
        if i + 2 <= gridSize:
            partition = arrWithoutHalo[i:i + 2, :]
        else:
            partition = arrWithoutHalo[i:gridSize, :]
        partitions.append(partition)

    # Expand each partition to make halo cells of 0 around it
    expandedPartitions = []
    for partition in partitions:
        expandedPartition = np.zeros((partition.shape[0] + 2, partition.shape[1] + 2))
        expandedPartition[1:-1, 1:-1] = partition
        expandedPartitions.append(expandedPartition)

    converged = False
    tolerance = 1e-6
    iteration = 0

    while not converged:
        results = pool.map(calculateTemp, expandedPartitions)

        # Update the grid with the results
        prevArr[1:gridSize + 1, 1:gridSize + 1] = arrWithoutHalo
        arrWithoutHalo = updateGrid(arrWithoutHalo, results, gridSize)

        # Check for convergence
        diff = np.abs(arrWithoutHalo - prevArr[1:gridSize + 1, 1:gridSize + 1])
        maxDiff = np.max(diff)
        if maxDiff < tolerance:
            converged = True

        # Update the expanded partitions with the new grid values
        for idx in range(len(expandedPartitions)):
            if 2 * idx + 2 <= gridSize:
                expandedPartitions[idx][1:-1, 1:-1] = arrWithoutHalo[2 * idx:2 * (idx + 1), :]
            else:
                expandedPartitions[idx][1:-1, 1:-1] = arrWithoutHalo[2 * idx:gridSize, :]

        iteration += 1
        print(f"Iteration {iteration}, max difference: {maxDiff}")
        print("Current grid state:")
        print(arrWithoutHalo)

    print("Final Result: ")
    print(arrWithoutHalo)

    pool.close()
    pool.join()

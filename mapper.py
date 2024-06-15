import sys
import numpy as np
import os

def calculateTemp(partition):
    newPartition = np.copy(partition)
    for i in range(1, partition.shape[0] - 1):
        for j in range(1, partition.shape[1] - 1):
            if partition[i, j] == 0:
                newPartition[i, j] = 0.25 * (partition[i - 1, j] + partition[i + 1, j] + partition[i, j - 1] + partition[i, j + 1])
    return newPartition

if __name__ == '__main__':
    partitionFile = sys.argv[1]
    partition = np.loadtxt(partitionFile, delimiter=',')
    newPartition = calculateTemp(partition)

    baseName = os.path.basename(partitionFile)
    newPartitionFile = f'new_{baseName}'

    np.savetxt(newPartitionFile, newPartition, delimiter=',')

    # Calculate convergence
    diff = np.abs(newPartition - partition)
    maxDiff = np.max(diff)
    converged = maxDiff < 1e-6

    # Output for reducer
    print(f'{baseName}\t{converged}')

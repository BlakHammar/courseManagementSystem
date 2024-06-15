import numpy as np
import sys

def combinePartitions(parts):
    combined = np.block([
        [parts[0][1:-1, 1:-1], parts[1][1:-1, 1:-1]],
        [parts[2][1:-1, 1:-1], parts[3][1:-1, 1:-1]]
    ])
    return combined

if __name__ == '__main__':
    parts = []
    converged = True
    for line in sys.stdin:
        partitionFile, partConverged = line.strip().split('\t')
        partConverged = partConverged == 'True'
        converged = converged and partConverged
        newPart = np.loadtxt(f'new_{partitionFile}', delimiter=',')
        parts.append(newPart)

    combinedGrid = combinePartitions(parts)
    np.savetxt('finalGrid.txt', combinedGrid, delimiter=',')  # Save the final grid regardless of convergence

    if converged:
        print("Converged")
        print(combinedGrid)
    else:
        step = combinedGrid.shape[0] // 2
        for i in range(2):
            for j in range(2):
                partition = combinedGrid[i*step:(i+1)*step, j*step:(j+1)*step]
                expandedPartition = np.pad(partition, pad_width=1, mode='constant', constant_values=0)
                np.savetxt(f'partition_{i*2+j}.txt', expandedPartition, delimiter=',')

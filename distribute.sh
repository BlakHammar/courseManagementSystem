#!/bin/bash

# Directory of the scripts
SCRIPT_DIR="/home/vboxuser/PycharmProjects/parallel/distribute"

# Activate the virtual environment if needed
source $SCRIPT_DIR/.venv/bin/activate

# Debug: Print current directory and list files
echo "Current directory: $(pwd)"
echo "Listing files in $SCRIPT_DIR:"
ls $SCRIPT_DIR

# Initialize the grid
echo "Initializing grid with temperature $1"
python3 $SCRIPT_DIR/preprocess.py $1

converged=false
while [ "$converged" = false ]; do
    echo "Running mappers"
    # Run mappers and redirect output to temporary file
    > $SCRIPT_DIR/mapperOutput.txt
    for i in {0..3}; do
        if [ -f "$SCRIPT_DIR/partition_$i.txt" ]; then
            echo "Processing partition_$i.txt"
            python3 $SCRIPT_DIR/mapper.py "$SCRIPT_DIR/partition_$i.txt" >> $SCRIPT_DIR/mapperOutput.txt
        else
            echo "Error: partition_$i.txt not found."
            exit 1
        fi
    done

    # Check if mapperOutput.txt was created and is not empty
    if [ ! -s "$SCRIPT_DIR/mapperOutput.txt" ]; then
        echo "Error: mapperOutput.txt is missing or empty."
        exit 1
    fi

    echo "Running reducer"
    # Run reducer
    if [ -f "$SCRIPT_DIR/mapperOutput.txt" ]; then
        python3 $SCRIPT_DIR/reducer.py < $SCRIPT_DIR/mapperOutput.txt > $SCRIPT_DIR/reducerOutput.txt
    else
        echo "Error: mapperOutput.txt not found."
        exit 1
    fi

    # Check for convergence
    if grep -q "Converged" $SCRIPT_DIR/reducerOutput.txt; then
        converged=true
    else
        converged=false
    fi

    # Clean up mapper output
    rm $SCRIPT_DIR/mapperOutput.txt
done

# Save final grid to a file
if [ -f "$SCRIPT_DIR/finalGrid.txt" ]; then
    echo "Final grid already saved."
else
    python3 $SCRIPT_DIR/reducer.py < $SCRIPT_DIR/mapperOutput.txt > $SCRIPT_DIR/finalGrid.txt
fi

# Visualize the final grid
if [ -f "$SCRIPT_DIR/finalGrid.txt" ]; then
    python3 $SCRIPT_DIR/visual.py $SCRIPT_DIR/finalGrid.txt $SCRIPT_DIR/finalGrid.png
else
    echo "Error: finalGrid.txt not found."
    exit 1
fi

# Clean up intermediary files
rm $SCRIPT_DIR/partition_*.txt $SCRIPT_DIR/new_partition_*.txt $SCRIPT_DIR/reducerOutput.txt

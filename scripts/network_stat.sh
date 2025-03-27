#!/bin/bash
# extract_network_stats.sh

# Navigate to the parent directory (gem5)
cd ..

# Check if m5out directory exists
if [ -d "m5out" ]; then
    # Create or overwrite network_stats.txt
    {
        echo "Extracted Network Statistics:"
        echo "-------------------------------"
        # Extract all lines containing the relevant metrics
        grep 'packets_injected' m5out/stats.txt >> m5out/network_stats.txt
        grep 'packets_received' m5out/stats.txt >> m5out/network_stats.txt
        grep 'packets_' m5out/stats.txt >> m5out/network_stats.txt
        grep 'average_' m5out/stats.txt >> m5out/network_stats.txt
        grep 'network_' m5out/stats.txt >> m5out/network_stats.txt
        grep 'flit_' m5out/stats.txt >> m5out/network_stats.txt # Example for flit stats
        echo "All relevant statistics extracted to m5out/network_stats.txt"
    } > m5out/network_stats.txt
else
    echo "m5out directory does not exist."
fi

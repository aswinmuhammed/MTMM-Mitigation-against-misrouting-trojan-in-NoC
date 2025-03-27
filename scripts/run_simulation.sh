#!/bin/bash

# Output files
full_stats_file="full_stats.txt"
plot_data_file="plot_data.txt"

# Clear the output files at the start
> "$full_stats_file"
> "$plot_data_file"

# Header for the full_stats file
printf "%-15s %-25s %-20s %-20s\n" "Injection Rate" "Average Packet Latency" "Packets Injected" "Packets Received" > "$full_stats_file"

# Loop through injection rates from 0.02 to 0.50 in increments of 0.02
for i in $(seq 1 25); do
    # Calculate the injection rate
    injection_rate=$(echo "scale=2; $i * 0.02" | bc)

    # Run the simulation
    echo "Running simulation with injection rate: $injection_rate"
    ~/gem5/build/NULL/gem5.opt \
    ~/gem5/configs/example/garnet_synth_traffic.py \
    --network=garnet --num-cpus=64 --num-dirs=64 --topology=Mesh_XY \
    --mesh-rows=8 --sim-cycles=1000000 --injectionrate=$injection_rate \
    --synthetic=bit_complement --routing-algorithm=1  # Use 1 for XY routing

    # Check if stats.txt exists before attempting to extract data
    if [ -f m5out/stats.txt ]; then
        # Extract the average packet latency from stats.txt
        avg_latency=$(grep 'average_packet_latency' m5out/stats.txt | awk '{print $2}')
        # Extract the number of packets injected from stats.txt
        packets_injected=$(grep 'packets_injected' m5out/stats.txt | awk '{print $2}')
        # Extract the number of packets received from stats.txt
        packets_received=$(grep 'packets_received' m5out/stats.txt | awk '{print $2}')

        # Append the data to the full_stats file with proper alignment
        printf "%-15s %-25s %-20s %-20s\n" "$injection_rate" "$avg_latency" "$packets_injected" "$packets_received" >> "$full_stats_file"

        # Append the data to the plot_data file in the specified format
        echo "$injection_rate: $avg_latency" >> "$plot_data_file"
    else
        # Append a placeholder if stats.txt is missing
        printf "%-15s %-25s %-20s %-20s\n" "$injection_rate" "N/A" "N/A" "N/A" >> "$full_stats_file"
    fi
done

echo "Simulation results saved to $full_stats_file and $plot_data_file"

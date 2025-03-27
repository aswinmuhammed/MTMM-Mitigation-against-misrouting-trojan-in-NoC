import re
import os

# Initialize variables to store extracted values
avg_packet_latency = None
avg_packet_network_latency = None
avg_packet_queueing_latency = None
packets_injected = None
packets_received = None

# Define regex patterns for latency and packet metrics
latency_pattern = re.compile(
    r'system\.ruby\.network\.(average_packet_latency|average_packet_network_latency|average_packet_queueing_latency)\s+(\d+\.?\d*)'
)
packet_injected_pattern = re.compile(
    r'system\.ruby\.network\.packets_injected::total\s+(\d+)'
)
packet_received_pattern = re.compile(
    r'system\.ruby\.network\.packets_received\s+\|\s+(\d+)'
)

# Path to the network stats file
stats_file_path = '../m5out/network_stats.txt'

# Check if the stats file exists
if os.path.isfile(stats_file_path):
    # Open the network_stats.txt file and extract the relevant data
    with open(stats_file_path, 'r') as file:
        lines = file.readlines()  # Read all lines into a list

        # Process the lines
        for line in lines:
            # Match latency values
            latency_match = latency_pattern.search(line)
            if latency_match:
                latency_type = latency_match.group(1)
                latency_value = float(latency_match.group(2))  # Convert to float for precision
                
                if latency_type == "average_packet_latency":
                    avg_packet_latency = latency_value
                elif latency_type == "average_packet_network_latency":
                    avg_packet_network_latency = latency_value
                elif latency_type == "average_packet_queueing_latency":
                    avg_packet_queueing_latency = latency_value

            # Match packets injected
            injected_match = packet_injected_pattern.search(line)
            if injected_match:
                packets_injected = int(injected_match.group(1))  # Convert to integer

            # Match packets received
            received_match = packet_received_pattern.search(line)
            if received_match:
                packets_received = int(received_match.group(1))  # Convert to integer

    # Print the extracted values for debugging
    print("Average Packet Latency:", avg_packet_latency)
    print("Average Packet Network Latency:", avg_packet_network_latency)
    print("Average Packet Queueing Latency:", avg_packet_queueing_latency)
    print("Packets Injected:", packets_injected)
    print("Packets Received:", packets_received)

    # Save the extracted values to uniform_random.txt
    uniform_random_file_path = '../m5out/uniform_random.txt'
    with open(uniform_random_file_path, 'a') as f:
        if avg_packet_latency is not None:
            f.write(f"Average Packet Latency: {avg_packet_latency}\n")
        if packets_injected is not None:
            f.write(f"Packets Injected: {packets_injected}\n")
        if packets_received is not None:
            f.write(f"Packets Received: {packets_received}\n")
else:
    print("Error: network_stats.txt not found.")

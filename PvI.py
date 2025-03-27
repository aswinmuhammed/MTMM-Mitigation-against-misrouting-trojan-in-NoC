import re
import matplotlib.pyplot as plt

# Function to parse stats.txt and extract data
def parse_stats(file_path):
    latency = []
    injection_rate = []
    with open(file_path, 'r') as file:
        for line in file:
            # Extract packet latency
            if "system.ruby.network.average_packet_latency" in line:  # Update based on your stats.txt
                match = re.search(r'\d+\.?\d*', line)
                if match:
                    latency.append(float(match.group()))
            # Extract injection rate
            if "system.ruby.network.injection_rate" in line:  # Update based on your stats.txt
                match = re.search(r'\d+\.?\d*', line)
                if match:
                    injection_rate.append(float(match.group()))
    return injection_rate, latency

# File path to stats.txt
stats_file = "m5out/stats.txt"  # Update with the actual path if needed

# Extract data
injection_rate, latency = parse_stats(stats_file)

# Check if data was successfully extracted
if not injection_rate or not latency:
    print("Error: Could not find matching data for injection rate or latency in stats.txt.")
else:
    # Plotting the data
    plt.figure(figsize=(8, 6))
    plt.plot(injection_rate, latency, marker='o', linestyle='-', color='b')
    plt.xlabel("Injection Rate (packets/cycle)")
    plt.ylabel("Packet Latency (cycles)")
    plt.title("Packet Latency vs Injection Rate")
    plt.grid(True)
    plt.show()


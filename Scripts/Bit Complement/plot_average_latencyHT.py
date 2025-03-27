import matplotlib.pyplot as plt

# Read data from the 'ht_graph_stats.txt' file
with open('ht_graph_stats.txt', 'r') as file:
    lines = file.readlines()  # Read lines from the file

# Prepare lists to hold injection rates and effective latencies
injection_rates = []
effective_latencies = []

# Parse the data from the file
for line in lines:
    if line.strip():  # Check if the line is not empty
        # Split the data into respective components
        parts = line.split(':')
        injection_rate = float(parts[0].strip())
        packets_without_ht = float(parts[1].strip())
        packets_with_ht = float(parts[2].strip())
        average_latency = float(parts[3].strip())

        # Calculate the effective average packet latency (EAPL)
        if packets_with_ht > 0:  # Avoid division by zero
            eapl = average_latency * (packets_without_ht / packets_with_ht)
            injection_rates.append(injection_rate)
            effective_latencies.append(eapl/500)

# Save injection rates and effective latencies to a text file
with open('ht.txt', 'w') as output_file:
    output_file.write("Injection Rate: Effective Packet Latency\n")
    for ir, eapl in zip(injection_rates, effective_latencies):
        output_file.write(f"{ir}: {eapl*500}\n")

# Plotting the Effective Average Packet Latency against the Injection Rates
plt.figure(figsize=(10, 6))
plt.plot(injection_rates, effective_latencies, marker='o', color='orange', label='Effective Latency')
plt.title('Effective Average Packet Latency vs. Injection Rate')
plt.xlabel('Injection Rate (packets/cycle)')
plt.ylabel('Effective Average Packet Latency (cycles)')
plt.grid()
plt.xlim(0.02, 0.50)  # Set x-axis limits
plt.xticks([round(i * 0.02, 2) for i in range(1, 26)])  # Adjust ticks to match the range

# Add a legend
plt.legend()

# Save the plot to a file
plt.savefig('effective_packet_latency_plot.png')
plt.close()  # Close the figure to free memory

print("Plot saved as 'effective_packet_latency_plot.png'")
print("Data saved as 'effective_packet_latencies.txt'")

import matplotlib.pyplot as plt

# Read data from the 'uniform_random.txt' file
with open('normal.txt', 'r') as file:
    lines = file.readlines()  # Read lines from the file

# Prepare lists to hold injection rates and latencies
injection_rates = []
latencies = []

# Parse the data from the file
for line in lines:
    if line.strip():  # Check if the line is not empty
        rate, latency = line.split(': ')
        injection_rates.append(float(rate))   # Convert rate to float
        latencies.append(float(latency) / 500)  # Convert latency to float

# Read data from the 'effective_packet_latencies.txt' file
with open('ht.txt', 'r') as file:
    lines = file.readlines()  # Skip the header line

# Prepare lists to hold effective latencies
effective_latencies = []

# Parse the data from the file
for line in lines:
    if line.strip():  # Check if the line is not empty
        rate, effective_latency = line.split(': ')
        effective_latencies.append(float(effective_latency)/500)  # Convert latency to float

# Plotting both graphs
plt.figure(figsize=(10, 6))

# Plot the average packet latencies
plt.plot(injection_rates, latencies, marker='o', label='Normal NOC (Bit_Complement)')

# Plot the effective packet latencies
plt.plot(injection_rates, effective_latencies, marker='s', color='orange', label='HT NOC (Bit_Complement)')

# Configure the graph
plt.title('Average Packet Latency vs. Injection Rate')
plt.xlabel('Injection Rate (packets/cycle)')
plt.ylabel('Latency (cycles)')
plt.grid()
plt.xlim(0.02, 0.50)  # Set x-axis limits
plt.xticks([round(i * 0.02, 2) for i in range(1, 26)])  # Adjust ticks to match the range

# Add a legend
plt.legend()

# Save the plot to a file
plt.savefig('combined_packet_latency_plot.png')
plt.close()  # Close the figure to free memory

print("Combined plot saved as 'combined_packet_latency_plot.png'")

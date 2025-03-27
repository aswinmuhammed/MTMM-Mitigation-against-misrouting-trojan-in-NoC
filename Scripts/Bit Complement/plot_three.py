import matplotlib.pyplot as plt

# Read data from the 'normal.txt' file
with open('normal.txt', 'r') as file:
    lines = file.readlines()

# Prepare lists to hold injection rates and latencies
injection_rates = []
latencies = []

# Parse the data from the file
for line in lines:
    if line.strip():  # Check if the line is not empty
        rate, latency = line.split(': ')
        injection_rates.append(float(rate))  # Convert rate to float
        latencies.append(float(latency) / 500)  # Convert latency to float

# Read data from the 'ht.txt' file
with open('ht.txt', 'r') as file:
    lines = file.readlines()

# Prepare lists to hold HT latencies
ht_latencies = []

# Parse the data from the file
for line in lines:
    if line.strip():  # Check if the line is not empty
        rate, effective_latency = line.split(': ')
        ht_latencies.append(float(effective_latency) / 500)  # Convert latency to float

# Read data from the 'mitigation.txt' file
with open('mitigation.txt', 'r') as file:
    lines = file.readlines()

# Prepare lists to hold mitigation latencies
mitigation_latencies = []

# Parse the data from the file
for line in lines:
    if line.strip():  # Check if the line is not empty
        rate, mitigation_latency = line.split(': ')
        mitigation_latencies.append(float(mitigation_latency) / 500)  # Convert latency to float

# Plotting all graphs
plt.figure(figsize=(10, 6))

# Plot the average packet latencies (normal)
plt.plot(injection_rates, latencies, marker='o', label='Normal NOC', color='blue')

# Plot the effective packet latencies (HT)
plt.plot(injection_rates, ht_latencies, marker='s', label='HT NOC', color='red')

# Plot the mitigation latencies
plt.plot(injection_rates, mitigation_latencies, marker='^', label='Mitigation NOC', color='green')

# Configure the graph
plt.title('Average Packet Latency vs. Injection Rate (Bit Complement)')
plt.xlabel('Injection Rate (packets/cycle)')
plt.ylabel('Latency (cycles)')
plt.grid()
plt.xlim(0.02, 0.20)  # Set x-axis limits
plt.xticks([round(i * 0.02, 2) for i in range(1, 11)])  # Adjust x-axis ticks
plt.ylim(10, 50)  # Set y-axis range from 0 to 50
plt.yticks(range(10, 101, 10))  # Adjust y-axis ticks with intervals of 5

# Add a legend
plt.legend()

# Save the plot to a file
plt.savefig('combined_packet_latency_with_mitigation.png')
plt.close()  # Close the figure to free memory

print("Combined plot saved as 'combined_packet_latency_with_mitigation.png'")

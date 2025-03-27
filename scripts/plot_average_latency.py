
import matplotlib.pyplot as plt

# Read data from the 'uniform_random.txt' file
with open('plot_data.txt', 'r') as file:
    lines = file.readlines()  # Read lines from the file

# Prepare lists to hold injection rates and latencies
injection_rates = []
latencies = []

# Parse the data from the file
for line in lines:
    if line.strip():  # Check if the line is not empty
        rate, latency = line.split(': ')
        injection_rates.append(float(rate))   # Convert rate to float
        latencies.append(float(latency)/500)     # Convert latency to float

# Plotting the average packet latency against the injection rates
plt.figure(figsize=(10, 6))
plt.plot(injection_rates, latencies, marker='o', label='Latency')
plt.title('Average Packet Latency vs. Injection Rate')
plt.xlabel('Injection Rate (packets/cycle)')
plt.ylabel('Average Packet Latency (cycles)')
plt.grid()
plt.xlim(0.02, 0.50)  # Set x-axis limits up to 0.2
plt.xticks([round(i * 0.02, 2) for i in range(1, 26)])  # Adjust ticks to match the range

# Add a legend
plt.legend()

# Save the plot to a file
plt.savefig('average_packet_latency_plot.png')
plt.close()  # Close the figure to free memory

print("Plot saved as 'average_packet_latency_plot.png'") 

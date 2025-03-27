import matplotlib.pyplot as plt

# Read data from the file
file_path = "thr.txt"
injection_rates = []
packets_received_baseline = []
packets_received_ht = []
packets_received_mitigation = []

with open(file_path, "r") as file:
    for line in file:
        parts = line.strip().split(":")
        if len(parts) == 4:
            injection_rates.append(float(parts[0]))  # Convert to float
            packets_received_baseline.append(int(parts[1]))  # Convert to int
            packets_received_ht.append(int(parts[2]))  # Convert to int
            packets_received_mitigation.append(int(parts[3]))  # Convert to int

# Normalize throughput separately for each dataset
max_baseline = max(packets_received_baseline)


throughput_baseline = [p / max_baseline for p in packets_received_baseline]
throughput_ht = [p / max_baseline for p in packets_received_ht]
throughput_mitigation = [p / max_baseline for p in packets_received_mitigation]

# Plot throughput graph
plt.figure(figsize=(8, 5))

# Baseline (Blue line with circles)
plt.plot(injection_rates, throughput_baseline, 'b-o', label="Baseline NoC", markersize=5, linewidth=1)

# HT (Red line with crosses)
plt.plot(injection_rates, throughput_ht, 'r-x', label="HT NoC", markersize=5, linewidth=1)

# Mitigation (Green line with triangles)
plt.plot(injection_rates, throughput_mitigation, 'g-^', label="Mitigation NoC", markersize=5, linewidth=1)

# Formatting the plot
plt.xlabel("Packet Injection Rate", fontsize=12)
plt.ylabel("Throughput", fontsize=12)
plt.title("Bit Complement", fontsize=14)
plt.legend(loc="upper left", fontsize=10)

# X-axis from 0.0 to 0.2 with proper tick marks
plt.xlim(0.02, 0.2)
plt.xticks([0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20])
plt.ylim(0.0, 0.6)
# Grid for readability
plt.grid(True, linestyle="--", alpha=0.6)

# Show the plot
plt.show()


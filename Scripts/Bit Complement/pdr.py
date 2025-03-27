import matplotlib.pyplot as plt

# Read data from the file
file_path = "pdr.txt"
injection_rates = []
baseline_latency = []
ht_latency = []
mitigation_latency = []
baseline_injected = []
baseline_received = []
ht_injected = []
ht_received = []
mitigation_injected = []
mitigation_received = []

with open(file_path, "r") as file:
    lines = file.readlines()

# Skip headers (first two lines)
data_lines = lines[2:]

for line in data_lines:
    parts = [x.strip() for x in line.split("|") if x.strip()]
    if len(parts) == 10:
        injection_rates.append(float(parts[0]))

        # Read latencies
        baseline_latency.append(float(parts[1]))
        ht_latency.append(float(parts[4]))
        mitigation_latency.append(float(parts[7]))

        # Read injected and received packets
        baseline_injected.append(int(parts[2]))
        baseline_received.append(int(parts[3]))
        ht_injected.append(int(parts[5]))
        ht_received.append(int(parts[6]))
        mitigation_injected.append(int(parts[8]))
        mitigation_received.append(int(parts[9]))

# Compute Deflected Packets Ejected
baseline_deflected = [inj - recv for inj, recv in zip(baseline_injected, baseline_received)]
ht_deflected = [inj - recv for inj, recv in zip(ht_injected, ht_received)]
mitigation_deflected = [inj - recv for inj, recv in zip(mitigation_injected, mitigation_received)]

# Compute EADPL for Baseline and Mitigation using the given formula
eadpl_baseline = [latency * (bd / hd) if hd != 0 else 0 
                   for latency, bd, hd in zip(baseline_latency, baseline_deflected, ht_deflected)]
eadpl_mitigation = [latency * (md / hd) if hd != 0 else 0 
                    for latency, md, hd in zip(mitigation_latency, mitigation_deflected, ht_deflected)]
eadpl_ht = ht_latency  # Directly from the data

# Plotting
plt.figure(figsize=(8, 5))
plt.plot(injection_rates, eadpl_baseline, marker='o', linestyle='-', color='blue', label="Baseline NoC")
plt.plot(injection_rates, eadpl_ht, marker='s', linestyle='-', color='red', label="HT NoC")
plt.plot(injection_rates, eadpl_mitigation, marker='^', linestyle='-', color='green', label="Mitigation NoC")

plt.xlabel("Packet Injection Rate")
plt.ylabel("Effective Average Deflected Packet Latency (Cycles)")
plt.title("Effective Average Deflected Packet Latency Comparison")
plt.legend()
plt.grid(True)

# Set x-axis limits dynamically
plt.xlim(0.05, 0.2)

# Auto-scale y-axis based on maximum calculated values
max_eadpl = max(eadpl_baseline + eadpl_ht + eadpl_mitigation) * 1.1
plt.ylim(0, max_eadpl)

plt.show()

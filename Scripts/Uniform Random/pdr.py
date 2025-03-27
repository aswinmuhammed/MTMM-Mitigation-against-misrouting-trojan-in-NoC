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
    next(file)  # Skip header line
    next(file)  # Skip separator line
    for line in file:
        parts = line.strip().split("|")
        if len(parts) == 10:
            injection_rates.append(float(parts[0].strip()))
            
            # Read latencies
            baseline_latency.append(float(parts[1].strip()))
            ht_latency.append(float(parts[4].strip()))
            mitigation_latency.append(float(parts[7].strip()))
            
            # Read injected and received packets
            baseline_injected.append(int(parts[2].strip()))
            baseline_received.append(int(parts[3].strip()))
            ht_injected.append(int(parts[5].strip()))
            ht_received.append(int(parts[6].strip()))
            mitigation_injected.append(int(parts[8].strip()))
            mitigation_received.append(int(parts[9].strip()))

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

# Set x-axis limit
plt.xlim(0.02, 0.2)

# Set y-axis limits and equally spaced ticks
plt.ylim(0, 10000)
plt.yticks([0, 2000, 4000, 6000, 8000, 10000])

plt.show()


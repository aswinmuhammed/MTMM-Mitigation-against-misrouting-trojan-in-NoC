import os

# Path to gem5 and benchmark binaries
gem5_exec = "./build/X86/gem5.opt"
script_path = "configs/deprecated/example/se.py"
binary_path = "/home/muhammed-aswin/gem5/binaries/cpu2017/binaries/"

# List of benchmarks
benchmarks = ["namd", "omnetpp"]

# Repeat benchmarks to fill 64 CPUs
cpu_count = 64
benchmarks *= (cpu_count // len(benchmarks)) + 1  # Repeat to fill 64 slots
benchmarks = benchmarks[:cpu_count]  # Trim to exactly 64

# Construct command
cmd = f"{gem5_exec} {script_path} --num-cpu={cpu_count} --cpu-type=DerivO3CPU --caches --l2cache --mem-type=SimpleMemory --maxinst=1000000 "

for bench in benchmarks:
    cmd += f'--cmd="{binary_path}{bench}" '

# Run command
print("Executing:", cmd)
os.system(cmd)

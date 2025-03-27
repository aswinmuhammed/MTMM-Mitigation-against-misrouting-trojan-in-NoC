from m5.objects import *
from m5 import *
from garnet2.routers import GarnetNetwork
from garnet2.networks import Mesh

# Create the system object
system = System()

# Set the clock and voltage domain
system.clk_domain = SrcClockDomain(clock="1GHz", voltage_domain=VoltageDomain(voltage="3.3V"))

# Set up memory
system.mem_mode = 'atomic'
system.mem_ranges = [AddrRange('512MB')]

# Create the CPU object
cpu = TimingSimpleCPU()
system.cpu = cpu
system.cpu.createThreads()

# Set up memory controller
mem_ctrl = DDR3_1600_8x8()
system.membus = SystemXBar()
mem_ctrl.port = system.membus.slave

# Create the Garnet network with mesh topology
noc = GarnetNetwork(network_id=0)
noc.topology = Mesh(width=8, height=8)  # 8x8 mesh topology
system.network = noc

# Connect the CPU to the network
system.cpu[0].connectAllPorts(system.membus)

# Set up the root object and start the simulation
root = Root(full_system=False, system=system)
m5.instantiate()
exit_event = m5.simulate()

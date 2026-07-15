# Low-Latency System Tuning — Finance & Real-Time

## Linux Kernel Tuning

### CPU & Scheduling

**CPU Isolation (kernel boot params):**
```bash
# /etc/default/grub — GRUB_CMDLINE_LINUX
isolcpus=4-7 nohz_full=4-7 rcu_nocbs=4-7 intel_pstate=disable
```

**CPU Governor:**
```bash
# Force performance mode
for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
    echo performance > "$cpu"
done

# Make permanent via systemd
# /etc/systemd/system/cpu-performance.service
[Unit]
Description=Set CPU governor to performance

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor'

[Install]
WantedBy=multi-user.target
```

**IRQ Affinity — Isolate network interrupts:**
```bash
# Find the NIC's IRQs
grep eth0 /proc/interrupts

# Assign the IRQ to a dedicated CPU (not the CPUs isolated for the app)
echo 2 > /proc/irq/<IRQ_NUM>/smp_affinity
# Or use irqbalance with --banirq to exclude
```

**Disable CPU C-States:**
```bash
# Boot param
intel_idle.max_cstate=0 processor.max_cstate=0

# Runtime
for cpu in /sys/devices/system/cpu/cpu*/cpuidle/state*/disable; do
    echo 1 > "$cpu"
done
```

### NUMA Awareness

```bash
# Check the NUMA topology
numactl --hardware
lstopo  # hwloc

# Run a process on a specific NUMA node
numactl --cpunodebind=0 --membind=0 ./my-trading-app

# Disable NUMA balancing (avoid migrations)
echo 0 > /proc/sys/kernel/numa_balancing
```

### Huge Pages

```bash
# Allocate 1024 huge pages of 2MB
echo 1024 > /proc/sys/vm/nr_hugepages

# Make permanent via sysctl
vm.nr_hugepages = 1024

# Transparent Huge Pages: disable for low-latency
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

# Verify
grep Huge /proc/meminfo
```

### Network — Ultra Low-Latency

**Busy Polling (eliminate interrupts):**
```bash
# sysctl
net.core.busy_read = 50        # microseconds
net.core.busy_poll = 50
```

**RSS (Receive Side Scaling) — spread traffic across CPUs:**
```bash
# Check support
ethtool -l eth0

# Set the number of queues
ethtool -L eth0 combined 4

# Queue-to-CPU affinity
# Use the driver's set_irq_affinity.sh (e.g., Intel ixgbe)
```

**Disable offloads if latency matters more than throughput:**
```bash
ethtool -K eth0 tso off gro off lro off
# Keep rx-checksumming and tx-checksumming ON
```

**Jumbo Frames:**
```bash
ip link set eth0 mtu 9000
# Verify end-to-end
ping -M do -s 8972 <destination>
```

---

## Windows Low-Latency

### CPU
```powershell
# Power plan: High Performance
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

# Disable Core Parking
powercfg -setacvalueindex SCHEME_CURRENT SUB_PROCESSOR CPMINCORES 100
powercfg -setactive SCHEME_CURRENT

# Processor affinity (via Process Explorer or programmatically)
$proc = Get-Process -Name "TradingApp"
$proc.ProcessorAffinity = 0xF0  # CPUs 4-7
```

### Network
```powershell
# Disable Nagle's Algorithm (registry, per interface)
# HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{GUID}
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" `
    -Name "TcpNoDelay" -Value 1 -Type DWord

# Disable TCP Chimney Offload
netsh int tcp set global chimney=disabled

# RSS
Enable-NetAdapterRss -Name "Ethernet"
Set-NetAdapterRss -Name "Ethernet" -BaseProcessorNumber 2 -MaxProcessors 4

# Interrupt Moderation (reduce for low latency)
Set-NetAdapterAdvancedProperty -Name "Ethernet" -RegistryKeyword "*InterruptModeration" -RegistryValue 0
```

### Timer Resolution
```powershell
# Force timer resolution to 0.5ms (instead of the default 15.6ms)
# Use a tool like TimerTool or programmatically via timeBeginPeriod(1)
# Warning: this impacts power consumption
```

---

## Benchmarking & Validation

| Test | Linux tool | Windows tool | Finance target |
|------|-------------|---------------|---------------|
| Network latency | `sockperf pp` | `latte.exe` | < 10us (same rack) |
| Throughput | `iperf3` | `iperf3` / `ntttcp` | > 90% line rate |
| Jitter | `cyclictest` | `LatencyMon` | < 5us p99 |
| Disk I/O | `fio` | `diskspd` | < 100us p99 (NVMe) |
| Context switch | `hackbench` | - | < 3us |

**cyclictest example (real-time validation):**
```bash
cyclictest -t4 -p99 -n -i1000 -l100000 --affinity=4-7
# -t4 : 4 threads
# -p99 : RT priority
# -i1000 : 1ms interval
# Target: max latency < 50us
```

---

## Finance pre-production checklist

- [ ] CPU isolation configured (isolcpus, nohz_full)
- [ ] CPU governor = performance
- [ ] C-States disabled
- [ ] NUMA-aware process placement
- [ ] Huge Pages allocated, THP disabled
- [ ] TCP tuning applied (BBR, buffer sizes)
- [ ] Busy polling enabled
- [ ] IRQ affinity configured
- [ ] Jumbo frames validated end-to-end
- [ ] Timer resolution adjusted (Windows)
- [ ] Benchmarks validated: p99 latency < threshold
- [ ] Monitoring in place: latency, jitter, packet loss
- [ ] RT kernel installed if needed (`PREEMPT_RT`)

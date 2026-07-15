# Data Transfer Patterns — Finance & Low-Latency

## Choosing the tool based on context

| Scenario | Linux | Windows | Cross-platform |
|----------|-------|---------|----------------|
| Local incremental sync | rsync | robocopy | rclone |
| Secure transfer | scp / sftp | WinSCP (CLI) | sftp |
| Cloud sync | rclone | rclone | rclone |
| High performance / bulk | rsync --compress | robocopy /MT:16 | bbcp, Aspera |
| Real-time streaming | netcat, socat, ncat | - | ZeroMQ, Kafka |
| Finance market data | multicast UDP | multicast UDP | Aeron, LMAX |

---

## rsync — Advanced patterns

**Incremental sync with logging and verification:**
```bash
rsync -avz --checksum --delete \
  --log-file=/var/log/rsync-$(date +%Y%m%d).log \
  --timeout=300 \
  --partial --partial-dir=.rsync-partial \
  --bwlimit=100M \
  -e "ssh -o StrictHostKeyChecking=yes -p 2222" \
  /data/source/ user@remote:/data/dest/
```

**Finance pipeline — sync every N seconds:**
```bash
#!/usr/bin/env bash
set -euo pipefail

INTERVAL=5  # seconds
SRC="/data/market-feed/"
DST="user@receiver:/data/incoming/"
LOCK="/var/run/market-sync.lock"

while true; do
    start=$(date +%s%N)

    if ! flock -n "$LOCK" rsync -az --inplace --whole-file \
        --timeout=10 "$SRC" "$DST" 2>>/var/log/market-sync.err; then
        echo "$(date) WARN: sync skipped (locked or failed)" >> /var/log/market-sync.log
    fi

    elapsed=$(( ($(date +%s%N) - start) / 1000000 ))
    sleep_ms=$((INTERVAL * 1000 - elapsed))
    [[ $sleep_ms -gt 0 ]] && sleep "$(echo "scale=3; $sleep_ms/1000" | bc)"
done
```

## robocopy — Advanced patterns

**Mirror with retry and logging:**
```powershell
robocopy "D:\Source" "\\server\Share\Dest" /MIR /Z /MT:16 `
    /R:3 /W:5 `
    /LOG+:C:\Logs\robocopy.log /TEE /NP `
    /XD ".git" "node_modules" `
    /MON:1 /MOT:1  # Monitor: rerun if a change is detected
```

---

## TCP optimization for high-performance transfers

### Linux sysctl tuning
```bash
# /etc/sysctl.d/90-network-perf.conf

# Buffer sizes (for 10Gbps+)
net.core.rmem_max = 67108864
net.core.wmem_max = 67108864
net.core.rmem_default = 1048576
net.core.wmem_default = 1048576
net.ipv4.tcp_rmem = 4096 1048576 67108864
net.ipv4.tcp_wmem = 4096 1048576 67108864

# Congestion control
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq

# Connection handling
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 65535

# Timestamps and SACK (disable for ultra-low-latency)
net.ipv4.tcp_timestamps = 1
net.ipv4.tcp_sack = 1

# Aggressive keep-alive for finance connections
net.ipv4.tcp_keepalive_time = 60
net.ipv4.tcp_keepalive_intvl = 10
net.ipv4.tcp_keepalive_probes = 5
```

### Windows TCP tuning
```powershell
# Enable TCP Auto-Tuning
Set-NetTCPSetting -SettingName Internet -AutoTuningLevelLocal Normal

# Enable RSS (Receive Side Scaling)
Enable-NetAdapterRss -Name "Ethernet0"

# Jumbo Frames (if the switch supports it)
Set-NetAdapterAdvancedProperty -Name "Ethernet0" -RegistryKeyword "*JumboPacket" -RegistryValue 9014

# Disable Nagle for low-latency
# (per application via the TCP_NODELAY socket option, recommended)
```

---

## Integrity verification

**Checksum-based transfer verification:**
```bash
# Sender side
find /data/batch/ -type f -exec sha256sum {} \; > /data/batch/MANIFEST.sha256
rsync -az /data/batch/ remote:/data/incoming/

# Receiver side
cd /data/incoming/ && sha256sum -c MANIFEST.sha256
```

**PowerShell equivalent:**
```powershell
# Sender
Get-ChildItem -Path D:\Batch -File -Recurse | ForEach-Object {
    [PSCustomObject]@{
        Path = $_.FullName.Replace('D:\Batch\','')
        Hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
    }
} | Export-Csv D:\Batch\MANIFEST.csv -NoTypeInformation

# Receiver
$manifest = Import-Csv \\server\incoming\MANIFEST.csv
$manifest | ForEach-Object {
    $actual = (Get-FileHash "\\server\incoming\$($_.Path)" -Algorithm SHA256).Hash
    if ($actual -ne $_.Hash) { Write-Warning "MISMATCH: $($_.Path)" }
}
```

---

## Pipeline monitoring

Critical metrics to watch:

| Metric | Alert threshold (finance) | Tool |
|----------|----------------------|-------|
| Transfer latency | > 100ms (same network) | Prometheus + custom exporter |
| Throughput | < 80% of link capacity | iftop, bmon, PerfMon |
| Failed files | > 0 | Checksum monitoring |
| Queue depth | > 1000 files | inotifywait, FileSystemWatcher |
| Jitter | > 5ms | ping -i 0.1 + stats |

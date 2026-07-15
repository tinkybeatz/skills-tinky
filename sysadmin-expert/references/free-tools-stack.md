# Free vs paid stack — Comparison by category

Always prioritize the "Recommended free" column. Only mention paid options if the user asks for them or if their needs exceed the limits of the free option.

## Monitoring & Metrics

| Recommended free | Paid alternative | When to pay |
|---|---|---|
| **Prometheus + Grafana** | Datadog ($15+/host/mo) | Zero-ops desired, correlated APM, team too small to maintain it |
| **Zabbix** (legacy/SNMP) | PRTG | Advanced hardware monitoring, heavy SNMP v3 |
| **Windows PerfMon + WEF** (native) | SolarWinds | Centralized multi-site Windows dashboards |

**Finance**: Prometheus supports microsecond histograms for p99/p999 tracking. Self-hosted = data on-prem (compliance data residency).

## Logs & Observability

| Recommended free | Paid alternative | When to pay |
|---|---|---|
| **Grafana Loki** | Splunk, Datadog Logs | Full-text search required across the entire corpus |
| **Graylog Open** (+ OpenSearch) | Graylog Enterprise | Advanced alerting, SIEM-like features |
| **ELK (Elasticsearch + Kibana)** | Elastic Cloud | Cluster management, automatic scaling |

**Finance**: Loki = 10x less storage than ELK (label-based indexing). If compliance requires full-text searchable audit trails → Graylog Open or ELK.

## Automation & Config Management

| Recommended free | Paid alternative | When to pay |
|---|---|---|
| **Ansible** (agentless, SSH) | Ansible Automation Platform | Centralized RBAC, UI, > 500 nodes |
| **Salt** (event-driven, ZeroMQ) | Salt Enterprise | Vendor support SLA |
| **Bash/PowerShell scripts** | - | Always free, < 10 machines |

**Finance**: Salt = event-driven, ideal for real-time remediation. Ansible = agentless, fewer daemons on trading servers.

**Selection rule**:
- < 5 machines → plain scripts
- 5-50 machines → Ansible
- 50+ machines with event-driven needs → Salt
- Windows only → PowerShell DSC + GPO

## Security & Compliance

| Recommended free | Paid alternative | When to pay |
|---|---|---|
| **Lynis** (Linux hardening audit) | - | Always free |
| **OpenSCAP** (CIS/SCAP compliance) | CIS-CAT Pro (~$1K/yr) | Auditor-ready reports, dashboard |
| **CIS-CAT Lite** (basic benchmarks) | Tenable (~$3.5K/yr/65 assets) | Continuous CVE scanning, asset discovery |
| **OSSEC / Wazuh** (HIDS) | CrowdStrike | Advanced EDR, threat intel |

**Finance**: PCI-DSS, SOX, and MAS TRM sometimes require vendor-supported reports. Open-source passes audits but requires more in-house documentation.

## Backup & Disaster Recovery

| Recommended free | Paid alternative | When to pay |
|---|---|---|
| **Restic** (encrypted, deduplicated, multi-backend) | Veeam ($1K-50K+/yr) | App-aware VM snapshots, instant recovery |
| **Borg** (SSH/local only) | Commvault | Enterprise orchestration, tape |
| **Duplicati** (GUI, cloud targets) | - | Alternative if a GUI is needed |

**Finance**: Restic = client-side encryption (data-at-rest compliance). For a trading DB → wrap pg_dump/mysqldump around restic. Veeam = instant VM recovery (RTO < 15min) for business-continuity compliance.

## Firewall & Network

| Recommended free | Paid alternative | When to pay |
|---|---|---|
| **nftables** (bare Linux, max perf) | - | Always free, more performant |
| **OPNsense** (appliance, IDS/IPS) | Palo Alto, Fortinet | L7 inspection, vendor support SLA |
| **pfSense CE** | pfSense Plus ($400+/yr) | Commercial Netgate support |
| **Suricata** (open IDS/IPS) | Snort (Cisco) | Integration with an enterprise security stack |

**Finance**: nftables on trading servers = lower latency (no intermediate appliance). OPNsense at the perimeter/office replaces Cisco ASA at zero cost.

## Certificates & PKI

| Recommended free | Paid alternative | When to pay |
|---|---|---|
| **Let's Encrypt** (ACME auto) | DigiCert, GlobalSign | EV certs, complex wildcards, specific compliance |
| **step-ca** (internal PKI) | Venafi | Multi-site enterprise PKI, automated rotation |
| **mkcert** (local dev) | - | Always free, dev only |

---

## Summary: a complete free stack

A finance sysadmin can operate with zero license cost:

```
Monitoring   : Prometheus + Grafana + Alertmanager
Logs         : Grafana Loki (or Graylog Open if full-text is required)
Automation   : Ansible + Bash/PowerShell scripts
Security     : Lynis + OpenSCAP + Wazuh
Backup       : Restic (or Borg if SSH-only)
Firewall     : nftables (servers) + OPNsense (perimeter)
Certificates : Let's Encrypt (public) + step-ca (internal)
```

**Triggers for switching to paid:**
1. A regulatory audit requiring vendor-supported reports
2. Scaling beyond what a small team can self-maintain
3. A need for app-aware features (APM, VM snapshots, L7 firewall)

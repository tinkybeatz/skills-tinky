# Organizing a sysadmin script library

## Directory structure

```
scripts/
├── linux/
│   ├── health/              # Health checks and diagnostics
│   │   ├── check-disk-usage.sh
│   │   ├── check-memory.sh
│   │   ├── check-services.sh
│   │   └── check-certificates.sh
│   ├── maintenance/         # Cleanup, rotation, updates
│   │   ├── rotate-logs.sh
│   │   ├── cleanup-tmp.sh
│   │   └── update-packages.sh
│   ├── security/            # Audit, hardening, compliance
│   │   ├── audit-permissions.sh
│   │   ├── audit-ssh-config.sh
│   │   ├── scan-open-ports.sh
│   │   └── check-cve.sh
│   └── provisioning/        # Installation and initial configuration
│       ├── setup-monitoring.sh
│       ├── setup-firewall.sh
│       └── setup-user.sh
├── windows/
│   ├── health/
│   │   ├── Check-DiskUsage.ps1
│   │   ├── Check-Services.ps1
│   │   └── Check-EventLog.ps1
│   ├── maintenance/
│   │   ├── Rotate-Logs.ps1
│   │   ├── Cleanup-TempFiles.ps1
│   │   └── Update-Software.ps1
│   ├── security/
│   │   ├── Audit-Permissions.ps1
│   │   ├── Audit-GPO.ps1
│   │   └── Check-Compliance.ps1
│   └── provisioning/
│       ├── Setup-Monitoring.ps1
│       ├── Setup-Firewall.ps1
│       └── Setup-ADUser.ps1
├── cross-platform/          # Ansible playbooks, Python
│   ├── playbooks/
│   │   ├── harden-server.yml
│   │   ├── deploy-monitoring.yml
│   │   └── rotate-certificates.yml
│   └── inventory/
│       ├── production.yml
│       └── staging.yml
└── lib/                     # Shared functions
    ├── common.sh            # Reusable Bash functions
    └── Common.psm1          # Shared PowerShell module
```

## Naming conventions

### Files
- **Bash**: `verb-noun.sh` in kebab-case (e.g. `check-disk-usage.sh`)
- **PowerShell**: `Verb-Noun.ps1` in PascalCase (e.g. `Check-DiskUsage.ps1`)
- **Ansible**: `verb-noun.yml` in kebab-case (e.g. `deploy-monitoring.yml`)
- **Prefix by category if outside the structure**: `sec-audit-ssh.sh`, `maint-rotate-logs.sh`

### Standard verbs
| Verb | Usage |
|-------|-------|
| `check-` / `Check-` | Verification, diagnostic, health check |
| `setup-` / `Setup-` | Installation and initial configuration |
| `update-` / `Update-` | Updating an existing configuration |
| `rotate-` / `Rotate-` | Rotating logs, certificates, secrets |
| `cleanup-` / `Cleanup-` | Cleaning up temporary files, caches |
| `audit-` / `Audit-` | Security audit, compliance |
| `backup-` / `Backup-` | Backing up data or configuration |
| `deploy-` / `Deploy-` | Deploying a service or application |
| `scan-` / `Scan-` | Scanning ports, vulnerabilities, files |

## Standard header (every script)

### Bash
```bash
#!/usr/bin/env bash
# -------------------------------------------------------------------
# check-disk-usage.sh — Checks disk space and alerts if usage exceeds a threshold
#
# Usage  : ./check-disk-usage.sh [--threshold 90] [--notify slack]
# Deps   : df, awk, curl (if --notify slack)
# Author : infra-team
# -------------------------------------------------------------------
set -euo pipefail
```

### PowerShell
```powershell
<#
.SYNOPSIS
    Checks disk space and alerts if usage is above the threshold.
.DESCRIPTION
    Check-DiskUsage monitors all volumes and sends an alert
    if usage exceeds the configured threshold.
.PARAMETER Threshold
    Usage percentage that triggers the alert (default: 90).
.EXAMPLE
    .\Check-DiskUsage.ps1 -Threshold 85
#>
[CmdletBinding()]
param(
    [int]$Threshold = 90
)
$ErrorActionPreference = 'Stop'
```

## Testing

| Language | Framework | Command |
|---------|-----------|----------|
| Bash | BATS | `bats tests/` |
| PowerShell | Pester | `Invoke-Pester -Path tests/` |
| Python | pytest | `pytest tests/` |
| Ansible | Molecule | `molecule test` |

### Test structure
```
tests/
├── linux/
│   └── check-disk-usage.bats
├── windows/
│   └── Check-DiskUsage.Tests.ps1
└── cross-platform/
    └── test_playbook.py
```

## Linting / Static analysis

| Tool | Language | Integration |
|-------|---------|-------------|
| **ShellCheck** | Bash | `shellcheck script.sh`, CI-integrable |
| **PSScriptAnalyzer** | PowerShell | `Invoke-ScriptAnalyzer -Path script.ps1` |
| **ansible-lint** | Ansible | `ansible-lint playbook.yml` |
| **pylint / ruff** | Python | `ruff check script.py` |

## Versioning

- Everything in git, every change via PR
- Semantic tags for production releases (`v1.0.0`, `v1.1.0`)
- `CHANGELOG.md` at the root of `scripts/`
- Branch `main` = production, `dev` = staging

## Detect-then-remediate pattern

Every health check produces an actionable exit code:

```bash
# check-disk-usage.sh
# Exit 0 = OK, Exit 1 = WARNING, Exit 2 = CRITICAL

usage=$(df / --output=pcent | tail -1 | tr -d ' %')
if [[ $usage -ge 95 ]]; then
    log "CRITICAL" "Disk usage at ${usage}%"
    # Auto-remediation
    /opt/scripts/linux/maintenance/cleanup-tmp.sh
    exit 2
elif [[ $usage -ge 85 ]]; then
    log "WARNING" "Disk usage at ${usage}%"
    exit 1
fi
exit 0
```

Scheduler: a systemd timer (Linux) or Task Scheduler (Windows) runs the health checks every 5 minutes and triggers automatic remediation if needed.

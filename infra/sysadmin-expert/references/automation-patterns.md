# Automation Patterns — Bash, PowerShell, Ansible

## Core principles

1. **Idempotence**: A script run twice produces the same result
2. **Error handling**: `set -euo pipefail` (Bash), `$ErrorActionPreference = 'Stop'` (PS)
3. **Logging**: Every action logged with a timestamp
4. **Dry-run**: Support a test mode when possible
5. **Notification**: Alert on failure (email, Slack, webhook)

---

## Bash — Base template

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- Config ---
readonly SCRIPT_NAME="$(basename "$0")"
readonly LOG_FILE="/var/log/${SCRIPT_NAME%.sh}.log"
readonly LOCK_FILE="/var/run/${SCRIPT_NAME%.sh}.lock"

# --- Functions ---
log() { printf '%s [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" "$2" | tee -a "$LOG_FILE"; }
die() { log "ERROR" "$1"; exit 1; }

cleanup() {
    rm -f "$LOCK_FILE"
    log "INFO" "Cleanup done"
}
trap cleanup EXIT

# Lock file (idempotence/concurrency)
if [[ -f "$LOCK_FILE" ]]; then
    die "Already running (lock: $LOCK_FILE)"
fi
echo $$ > "$LOCK_FILE"

# --- Main ---
log "INFO" "Starting $SCRIPT_NAME"

# ... logic here ...

log "INFO" "Completed successfully"
```

### Useful Bash patterns

**Retry with backoff:**
```bash
retry() {
    local max_attempts=$1; shift
    local delay=1
    for ((i=1; i<=max_attempts; i++)); do
        if "$@"; then return 0; fi
        log "WARN" "Attempt $i/$max_attempts failed, retrying in ${delay}s..."
        sleep $delay
        delay=$((delay * 2))
    done
    return 1
}
```

**Prerequisite checks:**
```bash
require_cmd() { command -v "$1" >/dev/null 2>&1 || die "Required command not found: $1"; }
require_root() { [[ $EUID -eq 0 ]] || die "Must run as root"; }
require_os() { [[ -f /etc/os-release ]] && grep -qi "$1" /etc/os-release || die "Unsupported OS (expected $1)"; }
```

---

## PowerShell — Base template

```powershell
#Requires -Version 5.1
#Requires -RunAsAdministrator
[CmdletBinding(SupportsShouldProcess)]
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$ScriptName = $MyInvocation.MyCommand.Name
$LogFile = "C:\Logs\$($ScriptName -replace '\.ps1$','').log"

function Write-Log {
    param([string]$Level, [string]$Message)
    $entry = "{0} [{1}] {2}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Level, $Message
    Add-Content -Path $LogFile -Value $entry
    Write-Host $entry
}

function Test-Prerequisite {
    param([string]$Command)
    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Command"
    }
}

try {
    Write-Log 'INFO' "Starting $ScriptName"

    if ($DryRun) {
        Write-Log 'INFO' '[DRY-RUN] No changes will be made'
    }

    # ... logic here ...

    Write-Log 'INFO' 'Completed successfully'
}
catch {
    Write-Log 'ERROR' $_.Exception.Message
    Write-Log 'ERROR' $_.ScriptStackTrace
    exit 1
}
```

### Useful PowerShell patterns

**Silent install with verification:**
```powershell
function Install-SoftwareSilent {
    param(
        [string]$InstallerPath,
        [string]$Arguments = '/S /v/qn',
        [string]$ExpectedExe
    )
    if ($ExpectedExe -and (Get-Command $ExpectedExe -ErrorAction SilentlyContinue)) {
        Write-Log 'INFO' "$ExpectedExe already installed, skipping"
        return
    }
    Start-Process -FilePath $InstallerPath -ArgumentList $Arguments -Wait -NoNewWindow
    if ($ExpectedExe -and -not (Get-Command $ExpectedExe -ErrorAction SilentlyContinue)) {
        throw "Installation failed: $ExpectedExe not found after install"
    }
}
```

---

## Ansible — Role structure

```
roles/
  my-role/
    defaults/main.yml    # Default variables (overridable)
    tasks/main.yml       # Main tasks
    handlers/main.yml    # Handlers (restart, reload)
    templates/           # Jinja2 files
    files/               # Static files
    vars/                # Specific variables
    meta/main.yml        # Role dependencies
```

### Ansible patterns

**Idempotent task with a handler:**
```yaml
- name: Configure sshd
  ansible.builtin.template:
    src: sshd_config.j2
    dest: /etc/ssh/sshd_config
    owner: root
    group: root
    mode: '0600'
    validate: '/usr/sbin/sshd -t -f %s'
  notify: restart sshd

# handlers/main.yml
- name: restart sshd
  ansible.builtin.systemd:
    name: sshd
    state: restarted
```

**Multi-OS with conditionals:**
```yaml
- name: Install monitoring packages
  ansible.builtin.package:
    name: "{{ monitoring_packages[ansible_os_family] }}"
    state: present

# defaults/main.yml
monitoring_packages:
  Debian: [prometheus-node-exporter, collectd]
  RedHat: [node_exporter, collectd]
```

**Post-deploy verification:**
```yaml
- name: Verify service is running
  ansible.builtin.systemd:
    name: "{{ service_name }}"
    state: started
  register: service_status

- name: Verify port is listening
  ansible.builtin.wait_for:
    port: "{{ service_port }}"
    timeout: 30
```

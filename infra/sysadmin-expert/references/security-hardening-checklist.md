# Security Hardening Checklist — Linux & Windows

## Linux (CIS-based)

### Authentication & Access
- [ ] Disable SSH root login (`PermitRootLogin no`)
- [ ] Configure SSH key-only auth (`PasswordAuthentication no`)
- [ ] SSH: non-standard port, `AllowUsers`, `MaxAuthTries 3`
- [ ] Configure sudoers with aliases (no direct `ALL=(ALL) ALL`)
- [ ] Enforce a password policy (`pam_pwquality`, `faillock`)
- [ ] Configure PAM: `pam_tally2` or `pam_faillock` to lock after N failures
- [ ] Disable unnecessary system accounts (`nologin` shell)
- [ ] Verify: `awk -F: '($3 == 0) {print}' /etc/passwd` (only root should be UID 0)

### Network & Firewall
- [ ] Default policy: DROP (iptables/nftables) or deny incoming (UFW)
- [ ] Open only the necessary ports
- [ ] Disable IPv6 if unused
- [ ] Sysctl: `net.ipv4.ip_forward=0` (except on a router)
- [ ] Sysctl: `net.ipv4.conf.all.rp_filter=1` (reverse path filtering)
- [ ] Sysctl: `net.ipv4.icmp_echo_ignore_broadcasts=1`
- [ ] Sysctl: `net.ipv4.conf.all.accept_redirects=0`

### Filesystem & Permissions
- [ ] `/tmp`, `/var/tmp` mounted with `noexec,nosuid,nodev`
- [ ] Check SUID/SGID: `find / -perm /6000 -type f 2>/dev/null`
- [ ] World-writable files: `find / -xdev -type f -perm -0002`
- [ ] Critical permissions: `/etc/shadow` 640, `/etc/passwd` 644
- [ ] Set `umask 027` by default

### Audit & Logging
- [ ] Install and configure `auditd`
- [ ] Audit rules: critical files, privileged commands, login/logout
- [ ] Log rotation with `logrotate`
- [ ] Forward logs to a central SIEM/syslog
- [ ] Protect the logs: append-only or remote shipping

### Patching & Updates
- [ ] Enable security auto-updates (`unattended-upgrades` / `dnf-automatic`)
- [ ] Schedule a maintenance window for kernel updates
- [ ] Check CVEs regularly (`openscap`, `lynis`)

### Services
- [ ] Disable unnecessary services: `systemctl list-unit-files --state=enabled`
- [ ] Each service runs as a dedicated user (not root)
- [ ] Configure systemd sandboxing: `ProtectSystem=strict`, `NoNewPrivileges=true`

---

## Windows Server (CIS-based)

### Authentication & Access
- [ ] Password policy: min length 14, complexity, history 24
- [ ] Account lockout: 5 attempts, 15 min lock
- [ ] Disable the local Administrator account (rename it at a minimum)
- [ ] Configure LAPS for local admin passwords
- [ ] Enable MFA for RDP and admin access
- [ ] Configure Credential Guard (Windows 10+/Server 2016+)

### Network & Firewall
- [ ] Windows Firewall ON on all profiles (Domain, Private, Public)
- [ ] Rules: block inbound by default, allow per service
- [ ] Disable SMBv1: `Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol`
- [ ] Configure SMB signing: `RequireSecuritySignature = $true`
- [ ] Disable NetBIOS over TCP/IP if unnecessary

### Policies & GPO
- [ ] Restrict logon: `Deny log on locally` for service accounts
- [ ] Configure User Rights Assignment per CIS
- [ ] AppLocker or WDAC for application whitelisting
- [ ] Disable PowerShell v2: `Disable-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2`
- [ ] Enable PowerShell ScriptBlock logging and Transcription

### Audit & Logging
- [ ] Configure Windows Advanced Audit Policy (not Basic)
- [ ] Enable: Logon/Logoff, Object Access, Policy Change, Privilege Use
- [ ] Event Log size: Security 4GB minimum
- [ ] Forward to a SIEM (WEF - Windows Event Forwarding)
- [ ] Protect the logs: restrictive permissions on `%SystemRoot%\System32\winevt\`

### Patching
- [ ] WSUS or Windows Update for Business configured
- [ ] Critical patch: < 72h in finance
- [ ] Monthly cycle: Patch Tuesday + test on staging
- [ ] Monthly compliance report

### Services
- [ ] Disable unnecessary services (Print Spooler if there's no printing, etc.)
- [ ] Critical services: gMSA instead of manual service accounts
- [ ] Verify: `Get-Service | Where-Object {$_.StartType -eq 'Automatic'}`

#!/usr/bin/env bash
# Read-only Linux system audit for Phase 1.
set -euo pipefail
printf '\n=== HOST ===\n'; hostnamectl 2>/dev/null || hostname
printf '\n=== KERNEL ===\n'; uname -a
printf '\n=== UPTIME ===\n'; uptime
printf '\n=== MEMORY ===\n'; free -h
printf '\n=== ROOT FILESYSTEM ===\n'; df -h /
printf '\n=== TOP PROCESSES ===\n'; ps -eo pid,ppid,stat,comm,%cpu,%mem --sort=-%cpu | head -n 11
printf '\nAudit complete. No system settings were changed.\n'

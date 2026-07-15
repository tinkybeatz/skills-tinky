#!/bin/bash
# Docker & Dokploy Diagnostic Inspector
# Usage: docker-inspect.sh <command> [args]
# Read-only diagnostic tool — does not modify any containers, volumes, or networks.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed or not in PATH${NC}"
    exit 1
fi

print_header() {
    echo -e "\n${BOLD}${BLUE}=== $1 ===${NC}\n"
}

print_warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_ok() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_err() {
    echo -e "${RED}✗ $1${NC}"
}

cmd_help() {
    cat <<EOF
Docker & Dokploy Diagnostic Inspector

Usage: docker-inspect.sh <command> [args]

Commands:
  overview          Full system overview (containers, images, disk, networks)
  health            Health check status of all containers
  network           Network analysis (dokploy-network, segmentation, DNS)
  resources         Resource usage (CPU, memory, disk) for all containers
  logs <name>       Last 100 log lines for a container (by name or ID)
  compose <file>    Validate a docker-compose.yml for Dokploy compatibility
  swarm             Swarm cluster status (nodes, services, tasks)
  disk              Disk usage analysis with cleanup recommendations
  ports             Port mapping and exposure analysis
  security          Security audit (non-root, capabilities, read-only, etc.)
  help              Show this help message

All commands are read-only and will not modify your system.
EOF
}

cmd_overview() {
    print_header "Docker System Info"
    docker version --format "Client: {{.Client.Version}} / Server: {{.Server.Version}}" 2>/dev/null || echo "Docker version unavailable"

    print_header "Running Containers"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}\t{{.Ports}}" 2>/dev/null || echo "No containers running"

    print_header "Stopped Containers"
    local stopped
    stopped=$(docker ps -a --filter "status=exited" --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" 2>/dev/null)
    if [ -n "$stopped" ] && [ "$(echo "$stopped" | wc -l)" -gt 1 ]; then
        echo "$stopped"
    else
        print_ok "No stopped containers"
    fi

    print_header "Images"
    docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}" 2>/dev/null | head -20

    print_header "Disk Usage"
    docker system df 2>/dev/null

    print_header "Networks"
    docker network ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}" 2>/dev/null

    print_header "Volumes"
    docker volume ls --format "table {{.Name}}\t{{.Driver}}" 2>/dev/null | head -20
}

cmd_health() {
    print_header "Container Health Status"

    docker ps --format '{{.Names}}' 2>/dev/null | while read -r name; do
        local health
        health=$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}no healthcheck{{end}}' "$name" 2>/dev/null)
        local status
        status=$(docker inspect --format '{{.State.Status}}' "$name" 2>/dev/null)

        case "$health" in
            healthy)
                print_ok "$name: $status ($health)"
                ;;
            unhealthy)
                print_err "$name: $status ($health)"
                # Show last health check log
                echo "  Last check:"
                docker inspect --format '{{range $i, $v := .State.Health.Log}}{{if eq $i 0}}  Exit: {{$v.ExitCode}} | Output: {{$v.Output}}{{end}}{{end}}' "$name" 2>/dev/null | head -3
                ;;
            starting)
                print_warn "$name: $status ($health)"
                ;;
            "no healthcheck")
                print_warn "$name: $status (no healthcheck configured)"
                ;;
        esac
    done
}

cmd_network() {
    print_header "Network Overview"
    docker network ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}" 2>/dev/null

    # Check dokploy-network
    print_header "Dokploy Network"
    if docker network inspect dokploy-network &>/dev/null; then
        print_ok "dokploy-network exists"
        echo ""
        echo "Connected containers:"
        docker network inspect dokploy-network --format '{{range .Containers}}  - {{.Name}} ({{.IPv4Address}}){{"\n"}}{{end}}' 2>/dev/null
    else
        print_warn "dokploy-network not found (not a Dokploy setup?)"
    fi

    # Check for internal networks
    print_header "Internal Networks (no external access)"
    docker network ls -q 2>/dev/null | while read -r net_id; do
        local name driver internal
        name=$(docker network inspect --format '{{.Name}}' "$net_id" 2>/dev/null)
        driver=$(docker network inspect --format '{{.Driver}}' "$net_id" 2>/dev/null)
        internal=$(docker network inspect --format '{{.Internal}}' "$net_id" 2>/dev/null)
        if [ "$internal" = "true" ]; then
            print_ok "$name ($driver) — internal: true"
        fi
    done

    # Check for containers NOT on dokploy-network that might need it
    print_header "Containers NOT on dokploy-network"
    if docker network inspect dokploy-network &>/dev/null; then
        local connected
        connected=$(docker network inspect dokploy-network --format '{{range .Containers}}{{.Name}} {{end}}' 2>/dev/null)
        docker ps --format '{{.Names}}' 2>/dev/null | while read -r name; do
            if ! echo "$connected" | grep -qw "$name"; then
                print_warn "$name is NOT on dokploy-network"
            fi
        done
    fi
}

cmd_resources() {
    print_header "Container Resource Usage"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}" 2>/dev/null

    print_header "Resource Limits"
    docker ps --format '{{.Names}}' 2>/dev/null | while read -r name; do
        local mem_limit cpu_limit
        mem_limit=$(docker inspect --format '{{.HostConfig.Memory}}' "$name" 2>/dev/null)
        cpu_limit=$(docker inspect --format '{{.HostConfig.NanoCpus}}' "$name" 2>/dev/null)

        local mem_str="unlimited"
        local cpu_str="unlimited"

        if [ "$mem_limit" != "0" ] && [ -n "$mem_limit" ]; then
            mem_str="$((mem_limit / 1048576))MB"
        fi
        if [ "$cpu_limit" != "0" ] && [ -n "$cpu_limit" ]; then
            cpu_str="$(echo "scale=1; $cpu_limit / 1000000000" | bc 2>/dev/null || echo "${cpu_limit}ns") CPUs"
        fi

        if [ "$mem_str" = "unlimited" ] && [ "$cpu_str" = "unlimited" ]; then
            print_warn "$name: no resource limits set"
        else
            echo "  $name: memory=$mem_str, cpu=$cpu_str"
        fi
    done
}

cmd_logs() {
    local container="${1:-}"
    if [ -z "$container" ]; then
        echo "Usage: docker-inspect.sh logs <container-name-or-id>"
        echo ""
        echo "Available containers:"
        docker ps -a --format "  {{.Names}} ({{.Status}})" 2>/dev/null
        exit 1
    fi

    print_header "Logs: $container (last 100 lines)"
    docker logs --tail 100 -t "$container" 2>&1
}

cmd_compose() {
    local file="${1:-docker-compose.yml}"
    if [ ! -f "$file" ]; then
        echo "File not found: $file"
        exit 1
    fi

    print_header "Dokploy Compatibility Check: $file"

    local issues=0

    # Check for container_name
    if grep -q "container_name:" "$file"; then
        print_err "container_name found — breaks Dokploy logs, metrics, and scaling"
        issues=$((issues + 1))
    else
        print_ok "No container_name"
    fi

    # Check for ports (should use expose)
    if grep -q "^[[:space:]]*ports:" "$file"; then
        print_warn "ports: found — use expose: instead (ports bypasses Traefik)"
        issues=$((issues + 1))
    else
        print_ok "No direct port publishing"
    fi

    # Check for dokploy-network
    if grep -q "dokploy-network" "$file"; then
        print_ok "dokploy-network referenced"
        # Check it's external
        if grep -A1 "dokploy-network:" "$file" | grep -q "external: true"; then
            print_ok "dokploy-network marked as external"
        else
            print_warn "dokploy-network should have 'external: true'"
            issues=$((issues + 1))
        fi
    else
        print_warn "dokploy-network not found — required for Traefik routing"
        issues=$((issues + 1))
    fi

    # Check for healthchecks
    if grep -q "healthcheck:" "$file"; then
        print_ok "Health checks found"
    else
        print_warn "No health checks — recommended for all services"
        issues=$((issues + 1))
    fi

    # Check for resource limits
    if grep -q "resources:" "$file" || grep -q "mem_limit:" "$file"; then
        print_ok "Resource limits found"
    else
        print_warn "No resource limits — recommended to prevent OOM"
        issues=$((issues + 1))
    fi

    # Check for restart policy
    if grep -q "restart:" "$file"; then
        print_ok "Restart policy found"
    else
        print_warn "No restart policy — recommended: 'restart: unless-stopped'"
        issues=$((issues + 1))
    fi

    # Check for .env references
    if grep -qE '\$\{[A-Z_]+\}' "$file"; then
        print_ok "Environment variable references found"
        print_warn "Reminder: Dokploy saves env vars to .env but doesn't auto-inject. Use env_file or \${VAR} syntax."
    fi

    echo ""
    if [ $issues -eq 0 ]; then
        print_ok "No issues found!"
    else
        echo -e "${YELLOW}Found $issues issue(s) to address${NC}"
    fi
}

cmd_swarm() {
    print_header "Swarm Status"

    local swarm_status
    swarm_status=$(docker info --format '{{.Swarm.LocalNodeState}}' 2>/dev/null)

    if [ "$swarm_status" != "active" ]; then
        print_warn "Swarm is not active (status: $swarm_status)"
        return
    fi

    print_ok "Swarm is active"
    echo ""

    print_header "Nodes"
    docker node ls 2>/dev/null || print_err "Cannot list nodes (not a manager?)"

    print_header "Services"
    docker service ls 2>/dev/null || print_err "Cannot list services"

    print_header "Service Details"
    docker service ls --format '{{.Name}}' 2>/dev/null | while read -r svc; do
        echo -e "${BOLD}$svc:${NC}"
        docker service ps --format "  {{.Name}}\t{{.CurrentState}}\t{{.Node}}\t{{.Error}}" "$svc" 2>/dev/null | head -5
        echo ""
    done
}

cmd_disk() {
    print_header "Docker Disk Usage"
    docker system df -v 2>/dev/null

    print_header "Cleanup Recommendations"

    local reclaimable
    reclaimable=$(docker system df --format '{{.Reclaimable}}' 2>/dev/null | head -1)
    echo "Reclaimable space: $reclaimable"
    echo ""
    echo "Commands to free space:"
    echo "  docker image prune -a --filter 'until=168h'  # Remove images older than 7 days"
    echo "  docker container prune                        # Remove stopped containers"
    echo "  docker builder prune -a                       # Remove build cache"
    echo "  docker system prune -a                        # Remove everything unused (CAREFUL)"
}

cmd_ports() {
    print_header "Port Mappings"
    docker ps --format "table {{.Names}}\t{{.Ports}}" 2>/dev/null

    print_header "Exposed-only Ports (internal, via Traefik)"
    docker ps -q 2>/dev/null | while read -r cid; do
        local name exposed published
        name=$(docker inspect --format '{{.Name}}' "$cid" 2>/dev/null | sed 's/^\/*//')
        exposed=$(docker inspect --format '{{range $p, $conf := .Config.ExposedPorts}}{{$p}} {{end}}' "$cid" 2>/dev/null)
        published=$(docker inspect --format '{{range $p, $conf := .NetworkSettings.Ports}}{{if $conf}}{{$p}} {{end}}{{end}}' "$cid" 2>/dev/null)

        if [ -n "$exposed" ]; then
            echo "  $name: exposed=$exposed published=${published:-none}"
        fi
    done
}

cmd_security() {
    print_header "Security Audit"

    docker ps --format '{{.Names}}' 2>/dev/null | while read -r name; do
        echo -e "\n${BOLD}$name:${NC}"

        # Check user
        local user
        user=$(docker inspect --format '{{.Config.User}}' "$name" 2>/dev/null)
        if [ -z "$user" ] || [ "$user" = "root" ] || [ "$user" = "0" ]; then
            print_err "  Running as root"
        else
            print_ok "  User: $user"
        fi

        # Check read-only
        local readonly
        readonly=$(docker inspect --format '{{.HostConfig.ReadonlyRootfs}}' "$name" 2>/dev/null)
        if [ "$readonly" = "true" ]; then
            print_ok "  Read-only rootfs"
        else
            print_warn "  Writable rootfs"
        fi

        # Check no-new-privileges
        local sec_opts
        sec_opts=$(docker inspect --format '{{.HostConfig.SecurityOpt}}' "$name" 2>/dev/null)
        if echo "$sec_opts" | grep -q "no-new-privileges"; then
            print_ok "  no-new-privileges"
        else
            print_warn "  no-new-privileges not set"
        fi

        # Check capabilities
        local cap_drop
        cap_drop=$(docker inspect --format '{{.HostConfig.CapDrop}}' "$name" 2>/dev/null)
        if echo "$cap_drop" | grep -qi "all"; then
            print_ok "  Capabilities: ALL dropped"
        else
            print_warn "  Capabilities not fully dropped ($cap_drop)"
        fi

        # Check privileged
        local privileged
        privileged=$(docker inspect --format '{{.HostConfig.Privileged}}' "$name" 2>/dev/null)
        if [ "$privileged" = "true" ]; then
            print_err "  PRIVILEGED MODE"
        fi
    done
}

# Main dispatch
case "${1:-help}" in
    overview)   cmd_overview ;;
    health)     cmd_health ;;
    network)    cmd_network ;;
    resources)  cmd_resources ;;
    logs)       cmd_logs "${2:-}" ;;
    compose)    cmd_compose "${2:-}" ;;
    swarm)      cmd_swarm ;;
    disk)       cmd_disk ;;
    ports)      cmd_ports ;;
    security)   cmd_security ;;
    help|--help|-h) cmd_help ;;
    *)
        echo "Unknown command: $1"
        echo ""
        cmd_help
        exit 1
        ;;
esac

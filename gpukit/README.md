# GPUKit - Dell R720 Dynamic Fan Speed Controller with GPU Support

GPUKit is a toolkit for managing Dell PowerEdge R720 servers with NVIDIA GPU support. It will likely work on other Dell PowerEdge servers. It was built for and tested with Nvidia Tesla P40 cards using nvidia-driver-550. The package provides dynamic fan speed control, GPU monitoring, and automated NVIDIA driver setup.

## Components

### dellfans
Dynamic fan speed controller that automatically adjusts fan speeds based on CPU and GPU temperatures. Runs as a systemd service.

**Features:**
- Monitors inlet, CPU, and GPU temperatures via IPMI and `nvidia-smi`
- Adjusts fan speed on a curve below the threshold; hands control back to factory auto above it
- Supports up to 2 NVIDIA GPUs (configurable)
- Logs to `/var/log/dellfans.log`

**Configuration via environment variables:**

| Variable | Default | Description |
|---|---|---|
| `INTERVAL_SEC` | `5` | Polling interval in seconds |
| `INITIAL_START_DELAY_SEC` | `10` | Startup delay before first poll |
| `MIN_FAN_PCT` | `10` | Minimum fan speed percentage |
| `MAX_FAN_PCT` | `100` | Maximum fan speed percentage |
| `GPU_COUNT` | `2` | Number of GPUs to monitor |
| `COLD_RESET` | `0` | Set to `1` to force IPMI cold reset on startup |

### dellfans-tool
CLI tool for querying and controlling the fan controller and IPMI subsystem.

**Usage:**
```bash
dellfans-tool <command>
```

| Command | Description |
|---|---|
| `status` | Show systemd service status |
| `temps` | Show current CPU, inlet, and GPU temperatures |
| `fans` | Show fan speeds in RPM |
| `logs [N]` | Show last N service log lines (default: 20) |
| `all` | Show all of the above |
| `ping` | Check if the IPMI controller is responsive |
| `reset` | Force a cold reset of the IPMI controller |

**Examples:**
```bash
sudo dellfans-tool temps
sudo dellfans-tool logs 50
sudo dellfans-tool ping
sudo dellfans-tool reset
```

### nvidia-rhel-setup
Automated setup script for installing and configuring NVIDIA GPU drivers and utilities on RHEL-based systems. Handles driver installation, CUDA toolkit setup, and nvidia-utils configuration.

**Usage:**
```bash
sudo nvidia-rhel-setup
```

### dellfans.service
Systemd service that runs `dellfans` as a background daemon. Installed and enabled automatically by the RPM.

```bash
sudo systemctl start dellfans.service
sudo systemctl stop dellfans.service
sudo systemctl restart dellfans.service
sudo systemctl status dellfans.service
```

## Building the RPM

### Prerequisites

```bash
sudo dnf install -y rpm-build rpmdevtools
```

### Build Steps

1. Navigate to the rpmbuild directory:
   ```bash
   cd gpukit/rpmbuild
   ```

2. Build the RPM:
   ```bash
   rpmbuild -ba --define "_topdir $(pwd)" SPECS/gpukit.spec
   ```

3. Locate the built RPM:
   - Binary RPM: `RPMS/noarch/gpukit-1.0-1.el*.noarch.rpm`
   - Source RPM: `SRPMS/gpukit-1.0-1.el*.src.rpm`

### Installation

```bash
sudo rpm -ivh RPMS/noarch/gpukit-1.0-1.el*.noarch.rpm
```

Upgrade if already installed:
```bash
sudo rpm -Uvh RPMS/noarch/gpukit-1.0-1.el*.noarch.rpm
```

## Installation from Source

```bash
sudo install -m 0755 rpmbuild/SOURCES/dellfans /usr/sbin/
sudo install -m 0755 rpmbuild/SOURCES/dellfans-tool /usr/sbin/
sudo install -m 0755 rpmbuild/SOURCES/nvidia-rhel-setup /usr/sbin/
sudo install -m 0644 rpmbuild/SOURCES/dellfans.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now dellfans.service
```

## Requirements

- **OS:** RHEL/CentOS 8 or later
- **Required:** `ipmitool`
- **Optional:** `nvidia-utils` (for GPU temperature monitoring)

```bash
sudo dnf install -y ipmitool
```

## Troubleshooting

**Service logs:**
```bash
sudo dellfans-tool logs 50
# or
journalctl -u dellfans.service -n 50
```

**IPMI not responding:**
```bash
sudo dellfans-tool ping
sudo dellfans-tool reset
```

**Fans running at unexpected speeds:**
Check the logs to see what temperature is driving the curve. The fan speed is derived from the highest temperature across all sensors (inlet, CPUs, GPUs).

**GPU not detected:**
```bash
nvidia-smi
# if drivers are missing:
sudo nvidia-rhel-setup
```

## License

MIT License

## Support

https://github.com/empthollow/scripts

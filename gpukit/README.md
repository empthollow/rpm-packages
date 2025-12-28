# GPUKit - Dell R720 Dynamic Fan Speed Controller with GPU Support

GPUKit is a comprehensive toolkit for managing Dell PowerEdge R720 servers with NVIDIA GPU support. It provides dynamic fan speed control, GPU monitoring, and automated NVIDIA driver setup.

## Components

### dellfans
Dynamic fan speed controller that automatically adjusts fan speeds based on CPU and GPU temperatures. 

**Features:**
- Monitors both CPU and GPU temperatures
- Automatic fan speed adjustment for optimal cooling and minimal noise
- Supports up to 2 NVIDIA GPUs via `nvidia-smi`
- Uses local IPMI for reliable temperature monitoring

**Usage:**
```bash
dellfans [options]
```

Run as a systemd service (see below) for continuous operation.

### dellfans-status
Monitor the current status of the dellfans service and system temperatures.

**Usage:**
```bash
dellfans-status
```

Displays current CPU/GPU temperatures and fan speeds.

### nvidia-rhel-setup
Automated setup script for installing and configuring NVIDIA GPU drivers and utilities on RHEL-based systems.

**Usage:**
```bash
nvidia-rhel-setup
```

Handles driver installation, CUDA toolkit setup, and nvidia-utils configuration.

### dellfans.service
Systemd service file for running dellfans as a background service.

**Starting the service:**
```bash
systemctl start dellfans.service
```

**Enabling on boot:**
```bash
systemctl enable dellfans.service
```

**Checking status:**
```bash
systemctl status dellfans.service
```

## Building the RPM

### Prerequisites

Ensure you have the RPM build tools installed:
```bash
sudo yum install -y rpm-build rpmdevtools
```

### Build Steps

1. **Navigate to the rpmbuild directory:**
   ```bash
   cd gpukit/rpmbuild
   ```

2. **Build the RPM:**
   ```bash
   rpmbuild -ba SOURCES/gpukit.spec
   ```

   Or using the spec file from SPECS directory:
   ```bash
   rpmbuild -ba SPECS/gpukit.spec
   ```

3. **Locate the built RPM:**
   - Binary RPM: `RPMS/noarch/gpukit-1.0-1.el*.noarch.rpm`
   - Source RPM: `SRPMS/gpukit-1.0-1.el*.src.rpm`

### Installation

Once built, install the RPM:
```bash
sudo rpm -ivh RPMS/noarch/gpukit-1.0-1.el*.noarch.rpm
```

Or upgrade if already installed:
```bash
sudo rpm -Uvh RPMS/noarch/gpukit-1.0-1.el*.noarch.rpm
```

## Installation from Source

If you prefer to install without building an RPM:

1. **Install the executables:**
   ```bash
   sudo install -m 0755 rpmbuild/SOURCES/dellfans /usr/sbin/
   sudo install -m 0755 rpmbuild/SOURCES/dellfans-status /usr/sbin/
   sudo install -m 0755 rpmbuild/SOURCES/nvidia-rhel-setup /usr/sbin/
   ```

2. **Install the systemd service:**
   ```bash
   sudo install -m 0644 rpmbuild/SOURCES/dellfans.service /etc/systemd/system/
   sudo systemctl daemon-reload
   ```

3. **Enable and start the service:**
   ```bash
   sudo systemctl enable dellfans.service
   sudo systemctl start dellfans.service
   ```

## Requirements

- **Base OS:** RHEL/CentOS 7 or later
- **Dependencies:**
  - `ipmitool` - for IPMI temperature and fan control
  - `nvidia-utils` - for GPU monitoring (optional but recommended)

Install dependencies:
```bash
sudo yum install -y ipmitool
```

For GPU support, also install:
```bash
sudo yum install -y nvidia-utils
```

Or use the included `nvidia-rhel-setup` script for automated NVIDIA driver installation.

## Configuration

The dellfans service runs automatically after installation. To customize behavior, you may need to edit the script directly or create a configuration file (if implemented).

## Troubleshooting

**Service won't start:**
```bash
systemctl status dellfans.service
journalctl -u dellfans.service -n 50
```

**Temperature monitoring issues:**
- Ensure `ipmitool` is installed and IPMI is enabled on the server
- Check IPMI permissions for the user running the service

**GPU not detected:**
- Run `nvidia-smi` to verify GPU drivers are installed
- Use `nvidia-rhel-setup` script if drivers need to be installed or updated

## License

MIT License

## Support

For issues or contributions, see the project repository at: https://github.com/empthollow/scripts

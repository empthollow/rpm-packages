Name:           gpukit
Version:        1.0
Release:        1%{?dist}
Summary:        Dell R720 Dynamic Fan Speed Controller with GPU support

License:        MIT
URL:            https://github.com/empthollow/scripts
Source0:        dellfans
Source1:        dellfans-status
Source2:        dellfans.service
Source3:        nvidia-rhel-setup

BuildArch:      noarch
Requires:       ipmitool
Suggests:       nvidia-utils

%description
Dynamic fan speed controller for Dell PowerEdge R720 servers. Monitors CPU and 
GPU temperatures and automatically adjusts fan speeds to maintain optimal cooling 
while minimizing noise. Uses local IPMI for reliable temperature monitoring and 
runs as a systemd service.

Supports up to 2 NVIDIA GPUs via nvidia-smi.

%install
install -D -m 0755 %{SOURCE0} %{buildroot}%{_sbindir}/dellfans
install -D -m 0755 %{SOURCE1} %{buildroot}%{_sbindir}/dellfans-status
install -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/dellfans.service
install -D -m 0755 %{SOURCE3} %{buildroot}%{_sbindir}/nvidia-rhel-setup

%pre
# Stop service if already running before upgrade
if systemctl is-active --quiet dellfans.service 2>/dev/null; then
    systemctl stop dellfans.service
fi

%post
# Reload systemd daemon and enable service
systemctl daemon-reload
systemctl enable dellfans.service
systemctl start dellfans.service

%preun
# Stop service before removal
if [ $1 -eq 0 ]; then
    systemctl stop dellfans.service
    systemctl disable dellfans.service
fi

%postun
# Reload systemd daemon after removal
systemctl daemon-reload

%files
%{_sbindir}/dellfans
%{_sbindir}/dellfans-status
%{_sbindir}/nvidia-rhel-setup
%{_unitdir}/dellfans.service

%changelog
* Sat Dec 27 2025 shoestring <user@localhost> - 1.0-1
- Initial release
- Dynamic fan control with GPU support
- Systemd service integration

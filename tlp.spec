# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: tlp
BuildArch: noarch
Epoch: 100
Version: 1.7.0
Release: 1%{?dist}
Summary: Optimize laptop battery life
License: GPL-2.0-or-later
URL: https://github.com/linrunner/TLP/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: make
BuildRequires: systemd
BuildRequires: udev
Requires: ethtool
Requires: hdparm
Requires: iw
Requires: pciutils
Requires: rfkill
Requires: systemd
Requires: udev
Requires: usbutils
Conflicts: laptop-mode-tools
Conflicts: power-profiles-daemon

%description
TLP is a feature-rich command-line utility, saving laptop battery power
without the need to delve deeper into technical details.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%make_build \
    TLP_SYSD=%{_unitdir} \
    TLP_ULIB=%{_udevrulesdir}/..

%install
%make_install \
    TLP_NMDSP=%{_prefix}/lib/NetworkManager/dispatcher.d \
    TLP_NO_INIT=1 \
    TLP_SDSL=%{_unitdir}/../system-sleep \
    TLP_SYSD=%{_unitdir} \
    TLP_ULIB=%{_udevrulesdir}/.. \
    TLP_WITH_ELOGIND=0 \
    TLP_WITH_SYSTEMD=1 \
    install install-man install-man-rdw

%package -n tlp-rdw
Summary: Radio device wizard
Requires: NetworkManager >= 1.20
Requires: tlp = %{epoch}:%{version}-%{release}

%description -n tlp-rdw
Radio device wizard is an add-on to TLP. It provides event based
switching of bluetooth, NFC, Wi-Fi and WWAN radio devices on:
  - network connect/disconnect
  - dock/undock

%files
%license LICENSE
%dir %{_sysconfdir}/tlp.d
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%config(noreplace) %{_sysconfdir}/tlp.conf
%config(noreplace) %{_sysconfdir}/tlp.d
%exclude %{_bindir}/tlp-rdw
%exclude %{_datadir}/bash-completion/completions/tlp-rdw
%exclude %{_datadir}/fish/vendor_completions.d/tlp-rdw.fish
%exclude %{_mandir}/man*/tlp-rdw*
%{_bindir}/*
%{_datadir}/bash-completion/completions/*
%{_datadir}/fish/vendor_completions.d/*
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/tlp
%{_datadir}/zsh/site-functions/*
%{_exec_prefix}/sbin/*
%{_mandir}/man*/*
%{_sharedstatedir}/tlp
%{_udevrulesdir}/../tlp-usb-udev
%{_udevrulesdir}/85-tlp.rules
%{_unitdir}/*.service
%{_unitdir}/../system-sleep

%files rdw
%license LICENSE
%dir %{_prefix}/lib/NetworkManager
%dir %{_prefix}/lib/NetworkManager/dispatcher.d
%{_bindir}/tlp-rdw
%{_datadir}/bash-completion/completions/tlp-rdw
%{_datadir}/fish/vendor_completions.d/tlp-rdw.fish
%{_mandir}/man*/tlp-rdw*
%{_prefix}/lib/NetworkManager/dispatcher.d/99tlp-rdw-nm
%{_udevrulesdir}/../tlp-rdw-udev
%{_udevrulesdir}/85-tlp-rdw.rules

%changelog

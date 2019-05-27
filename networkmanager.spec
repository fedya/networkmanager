%define url_ver %(echo %{version}|cut -d. -f1,2)

%define rname NetworkManager
%define api 1.0

%define majglib 4
%define libnm_glib %mklibname nm-glib %{majglib}
%define girclient %mklibname nmclient-gir %{api}
%define devnm_glib %mklibname -d nm-glib

%define majvpn 1
%define libnm_glib_vpn %mklibname nm-glib-vpn %{majvpn}
%define devnm_glib_vpn %mklibname -d nm-glib-vpn

%define majutil 2
%define libnm_util %mklibname nm-util %{majutil}
%define girname %mklibname %{name}-gir %{api}
%define devnm_util %mklibname -d nm-util

%define majlibnm 0
%define libnm %mklibname nm %{majlibnm}
%define nm_girname %mklibname nm-gir %{api}
%define devnm %mklibname -d nm
%define ppp_version 2.4.7

Name:		networkmanager
Summary:	Network connection manager and user applications
Version:	1.18.1
Release:	1
Group:		System/Base
License:	GPLv2+
Url:		http://www.gnome.org/projects/NetworkManager/
Source0:	https://download.gnome.org/sources/NetworkManager/%{url_ver}/%{rname}-%{version}.tar.xz
Source2:	00-server.conf

Patch3:		networkmanager-1.6.2-use-proper-ar-and-ranlib.patch

# from arch
Patch4:        0001-Add-Requires.private-glib-2.0.patch
#Patch5:	       shell-symbol-fetch-fix.patch

# OpenMandriva specific patches
Patch51:	networkmanager-0.9.8.4-add-systemd-alias.patch
Patch52:	networkmanager-1.16.0-clang-lto.patch
BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	gtk-doc
BuildRequires:	docbook-dtd42-xml
BuildRequires:	intltool
BuildRequires:	iptables
BuildRequires:	readline-devel
BuildRequires:	wpa_supplicant
BuildRequires:	libiw-devel
BuildRequires:	ppp-devel = %{ppp_version}
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(mm-glib)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-macros
BuildRequires:	pkgconfig(glibmm-2.4)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libndp)
BuildRequires:	pkgconfig(libnewt)
BuildRequires:	pkgconfig(mm-glib)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(libteamdctl)
BuildRequires:	pkgconfig(libteam)
BuildRequires:	pkgconfig(jansson)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	python3egg(pygobject)
BuildRequires:	pkgconfig(udev)
# For wext support
BuildRequires:	kernel-headers >= 4.11
#BuildRequires:	python-gobject3-devel
Requires:	iproute2
Requires:	iptables
Requires:	modemmanager
Requires:	ppp = %{ppp_version}
Requires(post,preun,postun):	rpm-helper
Requires:	wireless-tools
Requires:	wpa_supplicant >= 0.7.3-2
Suggests:	nscd
Provides:	NetworkManager = %{EVRD}
Obsoletes:	dhcdbd
Conflicts:	%{_lib}nm_util1 < 0.7.996
Conflicts:	initscripts < 9.24-5

%description
NetworkManager attempts to keep an active network connection available at all
times.  It is intended only for the desktop use-case, and is not intended for
usage on servers.   The point of NetworkManager is to make networking
configuration and setup as painless and automatic as possible.  If using DHCP,
NetworkManager is _intended_ to replace default routes, obtain IP addresses
from a DHCP server, and change nameservers whenever it sees fit.

%package -n %{libnm}
Summary:	Shared library for nm_util
Group:		System/Libraries

%description -n %{libnm}
Shared library for nm.

%package -n %{nm_girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{nm_girname}
GObject Introspection interface description for NM.

%package -n %{devnm}
Summary:	Development files for NM
Group:		Development/C
Provides:	nm-devel = %{EVRD}
Requires:	%{libnm} = %{EVRD}
Requires:	%{nm_girname} = %{EVRD}

%description -n %{devnm}
Development files for NM.

%package -n %{libnm_util}
Summary:	Shared library for nm_util
Group:		System/Libraries
Obsoletes:	%{mklibname networkmanager-util 0}
%rename		%{_lib}nm_util1

%description -n %{libnm_util}
Shared library for nm-util.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}nm-util2 < 0.9.8.0-2

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devnm_util}
Summary:	Development files for nm_util
Group:		Development/C
Obsoletes:	%{mklibname networkmanager-util 0 -d}
Provides:	nm-util-devel = %{EVRD}
Requires:	%{libnm_util} = %{EVRD}
Requires:	%{girname} = %{version}-%{release}
Obsoletes:	%{_lib}nm_util-devel < 0.7.996

%description -n %{devnm_util}
Development files for nm-util.

%package -n %{libnm_glib}
Summary:	Shared library for nm_glib
Group:		System/Libraries
Obsoletes:	%{mklibname networkmanager-glib 0}

%description -n %{libnm_glib}
This package contains the libraries that make it easier to use some
NetworkManager functionality from applications that use glib.

%package -n %{girclient}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}nm-glib4 < 0.9.8.0-2

%description -n %{girclient}
GObject Introspection interface description for %{name}.

%package -n %{devnm_glib}
Summary:	Development files for nm_glib
Group:		Development/C
Provides:	nm-glib-devel = %{EVRD}
Requires:	%{libnm_glib} = %{EVRD}
Requires:	%{girclient} = %{version}-%{release}
Obsoletes:	%{mklibname networkmanager-glib 0 -d}
Obsoletes:	%{_lib}nm_glib-devel < 0.7.996

%description -n %{devnm_glib}
Development files for nm-glib.

%package -n %{libnm_glib_vpn}
Summary:	Shared library for nm-glib-vpn
Group:		System/Libraries
Conflicts:	%{_lib}nm-glib1 < 0.7.996

%description -n %{libnm_glib_vpn}
This package contains the libraries that make it easier to use some
NetworkManager VPN functionality from applications that use glib.

%package -n %{devnm_glib_vpn}
Summary:	Development files for nm-glib-vpn
Group:		Development/C
Provides:	nm-glib-vpn-devel = %{EVRD}
Requires:	%{libnm_glib_vpn} = %{EVRD}
Conflicts:	%{_lib}nm_glib-devel < 0.7.996

%description -n %{devnm_glib_vpn}
Development files for nm-glib-vpn.

%prep
%autosetup -p1 -n %{rname}-%{version}

%build
%define _disable_ld_no_undefined 1

# --disable-qt below just disables a Qt 4.x based sample.
# plasma-nm is much nicer anyway.
%meson -Dsystemdsystemunitdir="%{_unitdir}" \
	-Dsystem_ca_path="%{_sysconfdir}/pki/tls/certs" \
	-Dudev_dir="/lib/udev" \
	-Diptables="/sbin/iptables" \
	-Ddist_version="%{version}-%{release}" \
	-Dsession_tracking=systemd \
	-Dsuspend_resume=systemd \
	-Dmodify_system=true \
	-Dpolkit_agent=true \
	-Dselinux=false \
	-Dconfig_logging_backend_default=journal \
	-Dlibaudit=no \
	-Diwd=true \
	-Dpppd_plugin_dir="%{_libdir}/pppd/%{ppp_version}" \
	-Dteamdctl=true \
	-Dlibnm_glib=true \
	-Dbluez5_dun=true \
	-Debpf=true \
	-Dconfig_plugins_default="ifcfg_rh" \
	-Difcfg_rh=true \
	-Dresolvconf="" \
	-Dconfig_dns_rc_manager_default=file \
	-Ddhclient="/sbin/dhclient" \
	-Ddhcpcd="/sbin/dhcpcd" \
	-Dconfig_dhcp_default=internal \
	-Dvapi=false \
	-Ddocs=true \
	-Dtests=no \
	-Dmore_logging=false \
	-Dld_gc=false \
	-Dcrypto=nss \
	-Dqt=false \
	-Db_lto=true

%meson_build

%install
%meson_install

# ifcfg-mdv currently broken, so just use ifcfg-rh for now untill it gets fixed
cat > %{buildroot}%{_sysconfdir}/NetworkManager/NetworkManager.conf << EOF
[main]
plugins=ifcfg-rh,keyfile
dhcp=internal
dns=default
rc-manager=file

[logging]
level=WARN
EOF

# Create netprofile module 
install -d %{buildroot}%{_sysconfdir}/netprofile/modules/
cat > %{buildroot}%{_sysconfdir}/netprofile/modules/01_networkmanager << EOF
# netprofile module
#
# this module contains settings for saving/restore the NetworkManager configuration
# in different network profiles

NAME="networkmanager"
DESCRIPTION="Networkmanager connection settings"

# list of files to be saved by netprofile
FILES="/etc/NetworkManager/"

# list of services to be restarted by netprofile
SERVICES="networkmanager"
EOF
chmod  755 %{buildroot}%{_sysconfdir}/netprofile/modules/01_networkmanager

install -m644 -p %{SOURCE2} -D %{buildroot}%{_sysconfdir}/NetworkManager/conf.d/00-server.conf

# create a VPN directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/VPN

install -m755 clients/.libs/nm-online -D %{buildroot}%{_bindir}/nm-online


# create keyfile plugin system-settings directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/system-connections

install -d %{buildroot}%{_prefix}/lib/%{rname}/conf.d/
install -d %{buildroot}%{_localstatedir}/lib/%{rname}/
touch %{buildroot}%{_localstatedir}/lib/%{rname}/%{rname}-intern.conf

# create a dnsmasq.d directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/dnsmasq.d
install -d %{buildroot}%{_sysconfdir}/%{rname}/dnsmasq-shared.d/

install -d %{buildroot}%{_datadir}/gnome-vpn-properties

install -d %{buildroot}%{_localstatedir}/lib/NetworkManager

# (tpg) Those are not required with systemd-udevd v210 or newer
rm -rf %{buildroot}/lib/udev/rules.d/84-nm-drivers.rules

#rhbz#974811
ln -sr %{buildroot}%{_unitdir}/NetworkManager-dispatcher.service %{buildroot}%{_unitdir}/dbus-org.freedesktop.nm-dispatcher.service

# (bor) clean up on uninstall
install -d %{buildroot}%{_localstatedir}/lib/%{rname}
pushd %{buildroot}%{_localstatedir}/lib/%{rname} && {
	touch %{rname}.state
	touch timestamps
popd
}

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable NetworkManager.service
enable NetworkManager-dispatcher.service
EOF

%find_lang %{rname}

%post

# bug 1395
# need to handle upgrade from minimal ifcfg files
# networkmanager < 0.9.10 treated a file with missing BOOTPROTO
# as BOOTPROTO=dhcp, later version treat it as IPV4 disabled
# so we add a BOOTPROTO to any ifcfg files without one
for x in /etc/sysconfig/network-scripts/ifcfg-*;
do
   if [ $(basename $x) != "ifcfg-lo" ]; then
       grep -q ^BOOTPROTO $x || echo BOOTPROTO=dhcp >> $x
   fi
done


%files -f %{rname}.lang
%doc AUTHORS CONTRIBUTING NEWS README TODO
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.NetworkManager.conf
%{_sysconfdir}/dbus-1/system.d/nm-dispatcher.conf
%{_sysconfdir}/dbus-1/system.d/nm-ifcfg-rh.conf
%dir %{_sysconfdir}/%{rname}
%config(noreplace) %{_sysconfdir}/%{rname}/NetworkManager.conf
%config(noreplace) %{_sysconfdir}/netprofile/modules/01_networkmanager
%dir %{_sysconfdir}/%{rname}/conf.d
%config(noreplace) %{_sysconfdir}/%{rname}/conf.d/00-server.conf
%dir %{_sysconfdir}/%{rname}/dispatcher.d
%dir %{_sysconfdir}/%{rname}/dnsmasq.d/
%dir %{_sysconfdir}/%{rname}/dnsmasq-shared.d/
%dir %{_sysconfdir}/%{rname}/system-connections
%dir %{_sysconfdir}/NetworkManager/VPN
%if %{_lib} != "lib64"
%dir %{_prefix}/lib/%{rname}
%else
%dir %{_libdir}/NetworkManager
%endif
%dir %{_prefix}/lib/%{rname}/conf.d/
%{_bindir}/nmcli
%{_bindir}/nmtui
%{_bindir}/nmtui-connect
%{_bindir}/nmtui-edit
%{_bindir}/nmtui-hostname
%{_bindir}/nm-online
%{_sbindir}/%{rname}
%{_libexecdir}/nm-dhcp-helper
%{_libexecdir}/nm-dispatcher
%{_libexecdir}/nm-iface-helper
%{_libexecdir}/nm-ifup
%{_libexecdir}/nm-ifdown
%{_libexecdir}/nm-initrd-generator
%dir %{_libdir}/NetworkManager
%dir %{_libdir}/NetworkManager/%{version}-%{release}
%{_libdir}/NetworkManager/%{version}-%{release}/*.so
%{_libdir}/pppd/*.*.*/nm-pppd-plugin.so
%dir %{_localstatedir}/lib/%{rname}
%ghost %{_localstatedir}/lib/%{rname}/*
%{_datadir}/bash-completion/completions/nmcli
%{_datadir}/dbus-1/interfaces/org.freedesktop.NetworkManager*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/polkit-1/actions/org.freedesktop.NetworkManager.policy
/lib/udev/rules.d/*.rules
%{_presetdir}/86-%{name}.preset
%{_unitdir}/NetworkManager-wait-online.service
%{_unitdir}/NetworkManager-dispatcher.service
%{_unitdir}/NetworkManager.service.d
%{_unitdir}/dbus-org.freedesktop.nm-dispatcher.service
%{_unitdir}/NetworkManager.service
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*
%{_datadir}/doc/NetworkManager/examples/server.conf

%files -n %{libnm}
%{_libdir}/libnm.so.%{majlibnm}*

%files -n %{nm_girname}
%{_libdir}/girepository-1.0/NM-%{api}.typelib

%files -n %{devnm}
%dir %{_includedir}/libnm
%{_includedir}/libnm/*.h
%doc %{_datadir}/gtk-doc/html/libnm
%{_datadir}/gir-1.0/NM-1.0.gir
%{_libdir}/pkgconfig/libnm.pc
%{_libdir}/libnm.so

%files -n %{libnm_util}
%{_libdir}/libnm-util.so.%{majutil}*

%files -n %{girname}
%{_libdir}/girepository-1.0/NetworkManager-%{api}.typelib

%files -n %{devnm_util}
%dir %{_includedir}/%{rname}
%{_includedir}/%{rname}/*.h
%doc %{_datadir}/gtk-doc/html/%{rname}
%doc %{_datadir}/gtk-doc/html/libnm-util
%{_datadir}/gir-1.0/NetworkManager-1.0.gir
%{_libdir}/pkgconfig/%{rname}.pc
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/libnm-util.so

%files -n %{libnm_glib}
%{_libdir}/libnm-glib.so.%{majglib}*

%files -n %{girclient}
%{_libdir}/girepository-1.0/NMClient-%{api}.typelib

%files -n %{libnm_glib_vpn}
%{_libdir}/libnm-glib-vpn.so.%{majvpn}*

%files -n %{devnm_glib}
%dir %{_includedir}/libnm-glib
%exclude %{_includedir}/libnm-glib/nm-vpn*.h
%doc %{_datadir}/gtk-doc/html/libnm-glib
%{_includedir}/libnm-glib/*.h
%{_libdir}/pkgconfig/libnm-glib.pc
%{_libdir}/libnm-glib.so
%{_datadir}/gir-1.0/NMClient-1.0.gir

%files -n %{devnm_glib_vpn}
%{_includedir}/libnm-glib/nm-vpn*.h
%{_libdir}/pkgconfig/libnm-glib-vpn.pc
%{_libdir}/libnm-glib-vpn.so

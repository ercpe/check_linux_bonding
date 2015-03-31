# Name of the plugin
%global plugin check_linux_bonding

# No binaries here, do not build a debuginfo package
%global debug_package %{nil}

# SUSE installs Nagios plugins under /usr/lib, even on 64-bit
# It also uses noarch for non-binary Nagios plugins and has different
# package names for docbook.
%if %{defined suse_version}
%global nagiospluginsdir /usr/lib/nagios/plugins
%global docbookpkg docbook-xsl-stylesheets
BuildArch:     noarch
%else
%global nagiospluginsdir %{_libdir}/nagios/plugins
%global docbookpkg docbook-style-xsl
%endif

Name:          nagios-plugins-bonding
Version:       1.4
Release:       1%{?dist}
Summary:       Nagios plugin to check Linux bonding interfaces

Group:         Applications/System
License:       GPLv3+
URL:           http://folk.uio.no/trondham/software/%{plugin}.html
Source0:       http://folk.uio.no/trondham/software/files/%{plugin}-%{version}.tar.gz

# Since we're also building for RHEL5
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Building requires Docbook XML
BuildRequires: libxslt
BuildRequires: libxml2
BuildRequires: %{docbookpkg}

# Owns the nagios plugins directory
Requires:      nagios-plugins

# Makes the transition to new package name easier for existing
# users of RPM packages
Provides:      check_linux_bonding = %{version}-%{release}
Obsoletes:     check_linux_bonding < 1.3.2

%description
check_linux_bonding is a plugin for Nagios that checks bonding
interfaces on Linux. The plugin is fairly simple and will report any
interfaces that are down (both masters and slaves). It will also alert
you of bonding interfaces with only one slave, since that usually
points to a misconfiguration.

%prep
%setup -q -n %{plugin}-%{version}

%build
pushd man
make clean && make
popd

%install
rm -rf %{buildroot}
install -Dp -m 0755 %{plugin} %{buildroot}%{nagiospluginsdir}/%{plugin}
install -Dp -m 0644 man/%{plugin}.8 %{buildroot}%{_mandir}/man8/%{plugin}.8

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc COPYING CHANGES
%{nagiospluginsdir}/%{plugin}
%{_mandir}/man8/%{plugin}.8*


%changelog
* Tue May 13 2014 Trond Hasle Amundsen <t.h.amundsen@usit.uio.no> - 1.4-1
- Release 1.4

* Fri Dec 14 2012 Trond Hasle Amundsen <t.h.amundsen@usit.uio.no> - 1.3.2-1
- Version 1.3.2
- New man page format
- New package name
- Fixed buildrequires and requires

* Tue Oct 26 2010 Trond Hasle Amundsen <t.h.amundsen@usit.uio.no> - 1.3.1-1
- Version 1.3.1

* Thu Aug 26 2010 Trond Hasle Amundsen <t.h.amundsen@usit.uio.no> - 1.3.0-1
- Version 1.3.0

* Wed Feb 17 2010 Trond Hasle Amundsen <t.h.amundsen@usit.uio.no> - 1.2.1-1
- Version 1.2.1

* Tue Feb 16 2010 Trond Hasle Amundsen <t.h.amundsen@usit.uio.no> - 1.2.0-1
- Version 1.2.0

* Thu Oct  9 2009 Trond Hasle Amundsen <t.h.amundsen@usit.uio.no> - 1.1.0-1
- Version 1.1.0
- Locations for plugin and man page changed

* Thu Jul 23 2009 Trond Hasle Amundsen <t.h.amundsen@usit.uio.no> - 1.0.1-1
- Version 1.0.1

* Wed Jun 10 2009 Trond Hasle Amundsen <t.h.amundsen@usit.uio.no> - 1.0.0-1
- Initial release 1.0.0

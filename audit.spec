#
# Conditional build:
%bcond_without	pie	# auditd as PIE binary
%bcond_without	python	# don't build python bindings
#
Summary:	User space tools for 2.6 kernel auditing
Summary(pl.UTF-8):	Narzędzia przestrzeni użytkownika do audytu jąder 2.6
Name:		audit
Version:	1.6.3
Release:	1
License:	GPL v2+
Group:		Daemons
Source0:	http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
# Source0-md5:	11f7c682093cea6aa6b2e6be93f9d0e3
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
Patch0:		%{name}-install.patch
URL:		http://people.redhat.com/sgrubb/audit/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
%{?with_pie:BuildRequires:	gcc >= 5:3.4}
BuildRequires:	gettext-devel >= 0.14.6
BuildRequires:	glibc-headers >= 6:2.3.6
BuildRequires:	intltool
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	linux-libc-headers >= 7:2.6.20
%if %{with python}
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
%endif
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
# use /lib, because this path is put in /usr/share/.../settings.py
%define		_libexecdir	%{_prefix}/lib

%description
The audit package contains the user space utilities for storing and
processing the audit records generate by the audit subsystem in the
Linux 2.6 kernel.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzia przestrzeni użytkownika do przechowywania
i przetwarzania rekordów audytu generowanych przez podsystem audytu w
jądrach Linuksa 2.6.

%package libs
Summary:	Dynamic audit libraries
Summary(pl.UTF-8):	Biblioteki dynamiczne audit
License:	LGPL v2.1+
Group:		Libraries

%description libs
The audit-libs package contains the dynamic libraries needed for
applications to use the audit framework.

%description libs -l pl.UTF-8
Ten pakiet zawiera biblioteki dynamiczne potrzebne dla aplikacji
używających środowiska audytu.

%package libs-devel
Summary:	Header files for audit libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek audit
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	linux-libc-headers >= 7:2.6.20

%description libs-devel
The audit-libs-devel package contains the header files needed for
developing applications that need to use the audit framework library.

%description libs-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia aplikacji
używających biblioteki środowiska audytu.

%package libs-static
Summary:	Static audit libraries
Summary(pl.UTF-8):	Statyczne biblioteki audit
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-libs-devel = %{version}-%{release}

%description libs-static
The audit-libs-static package contains the static libraries for
developing applications that need to use the audit framework.

%description libs-static -l pl.UTF-8
Ten pakiet zawiera statyczne biblioteki do tworzenia aplikacji
używających środowiska audytu.

%package audispd-plugins
Summary:	Plugins for the audit event dispatcher
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description audispd-plugins
The audispd-plugins package provides plugins for the real-time
interface to the audit system, audispd. These plugins can do things
like relay events to remote machines or analyze events for suspicious
behavior.

%package -n python-audit
Summary:	Python interface to libaudit library
Summary(pl.UTF-8):	Pythonowy interfejs do biblioteki libaudit
License:	LGPL v2.1+
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-audit
Python interface to libaudit library.

%description -n python-audit -l pl.UTF-8
Pythonowy interfejs do biblioteki libaudit.

%package -n system-config-audit
Summary:	Utility for editing audit configuration
Summary(pl.UTF-8):	Narzędzie do zmiany konfiguracji audytu
License:	GPL v2
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Version:	0.4.3
Requires:	python-pygtk-glade >= 2:2.0
Requires:	usermode
#Requires:	usermode-gtk	???

%description -n system-config-audit
An utility for editing audit configuration.

%description -n system-config-audit -l pl.UTF-8
Narzędzie do zmiany konfiguracji audytu.

%prep
%setup -q
%patch0 -p1

%if !%{with python}
sed 's#swig/Makefile ##' -i configure.ac
sed 's/swig//' -i Makefile.am
%endif

sed -i -e 's,/main\.py,/main.pyc,' system-config-audit/src/system-config-audit.in

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd system-config-audit
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
%configure \
	--with-apparmor
# override auditd_{C,LD}FLAGS to avoid -fPIE unsupported by gcc 3.3
%{__make} \
	%{!?with_pie:auditd_CFLAGS="-D_REENTRANT -D_GNU_SOURCE" auditd_LDFLAGS="-Wl,-z,relro"}

# temporarily not included in all
%{__make} -C auparse

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_var}/log/audit

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# temporarily not included in all
%{__make} -C auparse install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/libaudit.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libaudit.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libaudit.so
mv -f $RPM_BUILD_ROOT%{_libdir}/libauparse.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libauparse.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libauparse.so

# We manually install this since Makefile doesn't
install -d $RPM_BUILD_ROOT%{_includedir}
install lib/libaudit.h $RPM_BUILD_ROOT%{_includedir}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/auditd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/auditd

%if %{with python}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
rm -f $RPM_BUILD_ROOT%{py_sitescriptdir}/*.py
rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{la,a}

%py_postclean $RPM_BUILD_ROOT%{_datadir}/system-config-audit
%find_lang system-config-audit
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
/sbin/chkconfig --add auditd
%service auditd restart "audit daemon"

%preun
if [ "$1" = "0" ]; then
	%service auditd stop
	/sbin/chkconfig --del auditd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS TODO
%attr(750,root,root) %{_sbindir}/audispd
%attr(750,root,root) %{_sbindir}/auditctl
%attr(750,root,root) %{_sbindir}/auditd
%attr(750,root,root) %{_sbindir}/aureport
%attr(750,root,root) %{_sbindir}/ausearch
%attr(750,root,root) %{_sbindir}/autrace
%attr(755,root,root) %{_sbindir}/audispd-zos-remote
%dir %{_sysconfdir}/audisp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/audispd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/zos-remote.conf
%dir %{_sysconfdir}/audisp/plugins.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/af_unix.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/syslog.conf
%dir %{_sysconfdir}/audit
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/auditd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/audit.rules
%attr(754,root,root) /etc/rc.d/init.d/auditd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/auditd
%attr(750,root,root) %dir %{_var}/log/audit
%{_mandir}/man5/audispd.conf.5*
%{_mandir}/man5/auditd.conf.5*
%{_mandir}/man5/zos-remote.conf.5*
%{_mandir}/man8/*
%dir %{_sysconfdir}/audisp
%dir %{_sysconfdir}/audisp/plugins.d

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libaudit.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libaudit.so.0
%attr(755,root,root) /%{_lib}/libauparse.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libauparse.so.0
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libaudit.conf

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaudit.so
%attr(755,root,root) %{_libdir}/libauparse.so
%{_libdir}/libaudit.la
%{_libdir}/libauparse.la
%{_includedir}/auparse*.h
%{_includedir}/libaudit.h
%{_mandir}/man3/*

%files libs-static
%defattr(644,root,root,755)
%{_libdir}/libaudit.a
%{_libdir}/libauparse.a

%files audispd-plugins
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/audisp-ids
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/*.conf

%if %{with python}
%files -n python-audit
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_audit.so
%attr(755,root,root) %{py_sitedir}/auparse.so
%{py_sitedir}/auparse-*.egg-info
%{py_sitescriptdir}/audit.py[co]

%files -n system-config-audit -f system-config-audit.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/system-config-audit
%attr(755,root,root) %{_libexecdir}/system-config-audit-server
%{_datadir}/system-config-audit
%{_desktopdir}/system-config-audit.desktop
%endif

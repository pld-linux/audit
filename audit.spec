#
# Conditional build:
%bcond_without	pie	# auditd as PIE binary
#
Summary:	User space tools for 2.6 kernel auditing
Summary(pl):	Narzêdzia przestrzeni u¿ytkownika do audytu j±der 2.6
Name:		audit
Version:	1.1.4
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
# Source0-md5:	3a5f2a609b72de4101cc78f28c233a30
# http://people.redhat.com/sgrubb/audit/audit.h
Source1:	%{name}.h
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
Patch0:		%{name}-swig-fix.patch
URL:		http://people.redhat.com/sgrubb/audit/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.9
%{?with_pie:BuildRequires:	gcc >= 5:3.4}
BuildRequires:	glibc-headers >= 6:2.4
BuildRequires:	libtool
BuildRequires:	linux-libc-headers >= 2.6.11
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	swig-python
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The audit package contains the user space utilities for storing and
processing the audit records generate by the audit subsystem in the
Linux 2.6 kernel.

%description -l pl
Ten pakiet zawiera narzêdzia przestrzeni u¿ytkownika do przechowywania
i przetwarzania rekordów audytu generowanych przez podsystem audytu w
j±drach Linuksa 2.6.

%package libs
Summary:	Dynamic libaudit library
Summary(pl):	Biblioteka dynamiczna libaudit
License:	LGPL
Group:		Libraries

%description libs
The audit-libs package contains the dynamic library needed for
applications to use the audit framework.

%description libs -l pl
Ten pakiet zawiera bibliotekê dynamiczn± potrzebn± dla aplikacji
u¿ywaj±cych ¶rodowiska audytu.

%package libs-devel
Summary:	Header files for libaudit library
Summary(pl):	Pliki nag³ówkowe biblioteki libaudio
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	linux-libc-headers >= 7:2.6.12.0-4

%description libs-devel
The audit-libs-devel package contains the header files needed for
developing applications that need to use the audit framework library.

%description libs-devel -l pl
Ten pakiet zawiera pliki nag³ówkowe potrzebne do tworzenia aplikacji
u¿ywaj±cych biblioteki ¶rodowiska audytu.

%package libs-static
Summary:	Static libaudit library
Summary(pl):	Statyczna biblioteka libaudit
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs-devel = %{version}-%{release}

%description libs-static
The audit-libs-static package contains the static library for
developing applications that need to use the audit framework library.

%description libs-static -l pl
Ten pakiet zawiera statyczn± bibliotekê do tworzenia aplikacji
u¿ywaj±cych ¶rodowiska audytu.

%package -n python-audit
Summary:	Python interface to libaudit library
Summary(pl):	Pythonowy interfejs do biblioteki libaudit
License:	LGPL
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-audit
Python interface to libaudit library.

%description -n python-audit -l pl
Pythonowy interfejs do biblioteki libaudit.

%prep
%setup -q
%patch0 -p1

install -D %{SOURCE1} lib/linux/audit.h
install -D %{SOURCE1} src/mt/linux/audit.h

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
# override auditd_{C,LD}FLAGS to avoid -fPIE unsupported by gcc 3.3
%{__make} \
	%{!?with_pie:auditd_CFLAGS= auditd_LDFLAGS=}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_var}/log/audit

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/libaudit.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib} ; echo libaudit.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libaudit.so

# We manually install this since Makefile doesn't
install -d $RPM_BUILD_ROOT%{_includedir}
install lib/libaudit.h $RPM_BUILD_ROOT%{_includedir}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/auditd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/auditd

%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
rm -f $RPM_BUILD_ROOT%{py_sitescriptdir}/*.py
rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{la,a}

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
%doc AUTHORS ChangeLog README THANKS TODO sample.rules
%attr(750,root,root) %{_sbindir}/audispd
%attr(750,root,root) %{_sbindir}/auditctl
%attr(750,root,root) %{_sbindir}/auditd
%attr(750,root,root) %{_sbindir}/aureport
%attr(750,root,root) %{_sbindir}/ausearch
%attr(750,root,root) %{_sbindir}/autrace
%attr(754,root,root) /etc/rc.d/init.d/auditd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/auditd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit.rules
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/auditd
%attr(750,root,root) %dir %{_var}/log/audit
%{_mandir}/man8/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libaudit.so.*.*.*

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaudit.so
%{_libdir}/libaudit.la
%{_includedir}/libaudit.h
%{_mandir}/man3/*

%files libs-static
%defattr(644,root,root,755)
%{_libdir}/libaudit.a

%files -n python-audit
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_audit.so
%{py_sitescriptdir}/audit.py[co]

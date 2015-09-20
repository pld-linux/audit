#
# Conditional build:
%bcond_without	kerberos5	# Kerberos V support via heimdal
%bcond_without	prelude		# prelude audisp plugin
%bcond_without	golang		# Go language bindings
%bcond_without	python		# Python bindings (any)
%bcond_without	python3		# Python 3 bindings
%bcond_without	zos_remote	# zos-remote audisp plugin (LDAP dep)

%ifnarch %{ix86} %{x8664} %{arm}
%undefine	with_golang
%endif

%if %{without python}
%undefine	with_python3
%endif
Summary:	User space tools for 2.6 kernel auditing
Summary(pl.UTF-8):	Narzędzia przestrzeni użytkownika do audytu jąder 2.6
Name:		audit
Version:	2.4.4
Release:	1
License:	GPL v2+
Group:		Daemons
Source0:	http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
# Source0-md5:	72b0fd94d32846142bc472f0d91e62b4
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
Patch0:		%{name}-install.patch
Patch1:		%{name}-m4.patch
Patch2:		%{name}-nolibs.patch
Patch3:		%{name}-no_zos_remote.patch
Patch4:		%{name}-systemd-notonly.patch
Patch5:		%{name}-am.patch
Patch6:		%{name}-no-refusemanualstop.patch
Patch7:		%{name}-cronjob.patch
Patch8:		golang-paths.patch
# https://fedorahosted.org/fesco/ticket/1311
Patch9:		never-audit.patch
URL:		http://people.redhat.com/sgrubb/audit/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	glibc-headers >= 6:2.3.6
%{?with_golang:BuildRequires:	golang >= 1.4}
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	libcap-ng-devel
%{?with_prelude:BuildRequires:	libprelude-devel}
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	linux-libc-headers >= 7:2.6.30
%{?with_zos_remote:BuildRequires:	openldap-devel}
%if %{with python}
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
%endif
BuildRequires:	rpmbuild(macros) >= 1.623
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
Requires:	systemd-units >= 38
Obsoletes:	audit-audispd-plugins
Obsoletes:	audit-systemd
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
Requires:	linux-libc-headers >= 7:2.6.30

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

%package plugin-prelude
Summary:	prelude plugin for audispd
Summary(pl.UTF-8):	Wtyczka prelude dla audispd
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description plugin-prelude
audisp-prelude is a plugin for the audit event dispatcher daemon,
audispd, that uses libprelude to send IDMEF alerts for possible
Intrusion Detection events.

%description plugin-prelude -l pl.UTF-8
audisp-prelude to wtyczka demona audispd przekazującego zdarzenia
audytowe wykorzystująca libprelude do wysyłania alarmów IDMEF o
prawdopodobnych zdarzeniach IDS.

%package -n golang-audit
Summary:	Go language interface to libaudit library
Summary(pl.UTF-8):	Interfejs języka Go do biblioteki libaudit
License:	LGPL v2.1+
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Requires:	golang >= 1.4

%description -n golang-audit
Go language interface to libaudit library.

%description -n golang-audit -l pl.UTF-8
Interfejs języka Go do biblioteki libaudit.

%package -n python-audit
Summary:	Python 2.x interface to libaudit library
Summary(pl.UTF-8):	Interfejs Pythona 2.x do biblioteki libaudit
License:	LGPL v2.1+
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-audit
Python 2.x interface to libaudit library.

%description -n python-audit -l pl.UTF-8
Interfejs Pythona 2.x do biblioteki libaudit.

%package -n python3-audit
Summary:	Python 3.x interface to libaudit library
Summary(pl.UTF-8):	Interfejs Pythona 3.x do biblioteki libaudit
License:	LGPL v2.1+
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python3-audit
Python 3.x interface to libaudit library.

%description -n python3-audit -l pl.UTF-8
Interfejs Pythona 3.x do biblioteki libaudit.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%{!?with_zos_remote:%patch3 -p1}
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%if %{without python}
sed 's#swig/Makefile ##' -i configure.ac
sed 's/swig//' -i Makefile.am
%endif

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_kerberos5:--enable-gssapi-krb5} \
	--enable-systemd \
	--with-apparmor \
	--with-libwrap \
	%{?with_prelude:--with-prelude}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_var}/log/audit

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/auditd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/auditd

install -d $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/libaudit.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libaudit.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libaudit.so
mv -f $RPM_BUILD_ROOT%{_libdir}/libauparse.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libauparse.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libauparse.so

# RH initscripts-specific
%{__rm} -r $RPM_BUILD_ROOT%{_libexecdir}/initscripts

%if %{with python}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.{la,a}
%endif

%if %{with python3}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.{la,a}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
# Copy default rules into place on new installation
if [ ! -e %{_sysconfdir}/audit/audit.rules ] ; then
	cp -a %{_sysconfdir}/audit/rules.d/audit.rules %{_sysconfdir}/audit/audit.rules
fi
/sbin/chkconfig --add auditd
%service auditd restart "audit daemon"
%systemd_post auditd.service

%preun
if [ "$1" = "0" ]; then
	%service auditd stop
	/sbin/chkconfig --del auditd
fi
%systemd_preun auditd.service

%postun
%systemd_reload

%triggerpostun -- %{name} < 2.2-2
%systemd_trigger auditd.service

%triggerpostun -- %{name} < 2.3-1
if [ -e %{_sysconfdir}/audit/audit.rules.rpmsave ] ; then
	%{__mv} %{_sysconfdir}/audit/audit.rules{.rpmsave,}
fi
%service auditd restart "audit daemon"
%systemd_post auditd.service

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS TODO
%doc contrib/{capp,nispom,lspp,stig}.rules init.d/auditd.cron
%attr(750,root,root) %{_bindir}/aulast
%attr(750,root,root) %{_bindir}/aulastlog
%attr(750,root,root) %{_bindir}/ausyscall
%attr(750,root,root) %{_bindir}/auvirt
%attr(750,root,root) %{_sbindir}/audispd
%attr(750,root,root) %{_sbindir}/auditctl
%attr(750,root,root) %{_sbindir}/auditd
%attr(750,root,root) %{_sbindir}/augenrules
%attr(750,root,root) %{_sbindir}/aureport
%attr(750,root,root) %{_sbindir}/ausearch
%attr(750,root,root) %{_sbindir}/autrace
%attr(755,root,root) %{_sbindir}/audisp-remote
%{?with_zos_remote:%attr(755,root,root) %{_sbindir}/audispd-zos-remote}
%dir %{_sysconfdir}/audisp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/audispd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/audisp-remote.conf
%{?with_zos_remote:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/zos-remote.conf}
%dir %{_sysconfdir}/audisp/plugins.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/af_unix.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/au-remote.conf
%{?with_zos_remote:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/audispd-zos-remote.conf}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/syslog.conf
%dir %{_sysconfdir}/audit
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/auditd.conf
%dir %{_sysconfdir}/audit/rules.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/rules.d/audit.rules
%attr(754,root,root) /etc/rc.d/init.d/auditd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/auditd
%{systemdunitdir}/auditd.service
%attr(750,root,root) %dir %{_var}/log/audit
%{_mandir}/man5/audispd.conf.5*
%{_mandir}/man5/audisp-remote.conf.5*
%{_mandir}/man5/auditd.conf.5*
%{_mandir}/man5/ausearch-expression.5*
%{?with_zos_remote:%{_mandir}/man5/zos-remote.conf.5*}
%{_mandir}/man7/audit.rules.7*
%{_mandir}/man8/audisp-remote.8*
%{?with_zos_remote:%{_mandir}/man8/audispd-zos-remote.8*}
%{_mandir}/man8/audispd.8*
%{_mandir}/man8/auditctl.8*
%{_mandir}/man8/auditd.8*
%{_mandir}/man8/augenrules.8*
%{_mandir}/man8/aulast.8*
%{_mandir}/man8/aulastlog.8*
%{_mandir}/man8/aureport.8*
%{_mandir}/man8/ausearch.8*
%{_mandir}/man8/ausyscall.8*
%{_mandir}/man8/autrace.8*
%{_mandir}/man8/auvirt.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libaudit.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libaudit.so.1
%attr(755,root,root) /%{_lib}/libauparse.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libauparse.so.0
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libaudit.conf
%{_mandir}/man5/libaudit.conf.5*

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaudit.so
%attr(755,root,root) %{_libdir}/libauparse.so
%{_libdir}/libaudit.la
%{_libdir}/libauparse.la
%{_includedir}/auparse*.h
%{_includedir}/libaudit.h
%{_pkgconfigdir}/audit.pc
%{_pkgconfigdir}/auparse.pc
%{_mandir}/man3/audit_*.3*
%{_mandir}/man3/auparse_*.3*
%{_mandir}/man3/ausearch_*.3*
%{_mandir}/man3/get_auditfail_action.3*
%{_mandir}/man3/set_aumessage_mode.3*

%files libs-static
%defattr(644,root,root,755)
%{_libdir}/libaudit.a
%{_libdir}/libauparse.a

%if %{with prelude}
%files plugin-prelude
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/audisp-prelude
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/audisp-prelude.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/au-prelude.conf
%{_mandir}/man5/audisp-prelude.conf.5*
%{_mandir}/man8/audisp-prelude.8*
%endif

%if %{with golang}
%files -n golang-audit
%defattr(644,root,root,755)
%dir %{_libdir}/golang/src/redhat.com
%{_libdir}/golang/src/redhat.com/audit
%endif

%if %{with python}
%files -n python-audit
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_audit.so
%attr(755,root,root) %{py_sitedir}/auparse.so
%{py_sitedir}/audit.py[co]
%endif

%if %{with python3}
%files -n python3-audit
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_audit.so
%attr(755,root,root) %{py3_sitedir}/auparse.so
%{py3_sitedir}/audit.py
%endif

#
# Conditional build:
%bcond_without	kerberos5	# Kerberos V support via heimdal
%bcond_without	golang		# Go language bindings
%bcond_with	gccgo		# use GCC go frontend instead of golang implementation
%bcond_without	python		# Python bindings (any)
%bcond_without	python2		# Python 2 bindings
%bcond_without	python3		# Python 3 bindings
%bcond_without	zos_remote	# zos-remote audisp plugin (LDAP dep)

%ifnarch %{ix86} %{x8664} %{arm} aarch64 mips64 mips64le ppc64 ppc64le s390x
%define		with_gccgo	1
%endif

%if %{without python}
%undefine	with_python2
%undefine	with_python3
%endif

%if %{_ver_ge %(rpm -q --qf='%%{E}:%%{V}' linux-libc-headers) 7:5.17}
%define		with_flex_array_fix	1
%endif
Summary:	User space tools for 2.6 kernel auditing
Summary(pl.UTF-8):	Narzędzia przestrzeni użytkownika do audytu jąder 2.6
Name:		audit
Version:	3.1.1
Release:	2
License:	GPL v2+
Group:		Daemons
Source0:	https://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
# Source0-md5:	75363550690ee057f2fcf4f13eddcb4d
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
Patch0:		%{name}-install.patch
Patch2:		%{name}-nolibs.patch
Patch3:		%{name}-systemd-notonly.patch
Patch5:		%{name}-no-refusemanualstop.patch
Patch7:		golang-paths.patch
Patch8:		%{name}-flex-array-workaround.patch
Patch9:		%{name}-undo-flex-array.patch
URL:		http://people.redhat.com/sgrubb/audit/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.12.6
BuildRequires:	glibc-headers >= 6:2.3.6
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	libcap-ng-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libwrap-devel
BuildRequires:	linux-libc-headers >= 7:2.6.30
%{?with_zos_remote:BuildRequires:	openldap-devel}
%if %{with python2}
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
%endif
BuildRequires:	rpmbuild(macros) >= 1.750
BuildRequires:	sed >= 4.0
%if %{with golang}
%{?with_gccgo:BuildRequires:	gcc-go >= 5.1}
%{!?with_gccgo:BuildRequires:	golang >= 1.4}
%endif
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
Requires:	systemd-units >= 38
Obsoletes:	audit-audispd-plugins < 1.6.7
Obsoletes:	audit-plugin-prelude < 3
Obsoletes:	audit-systemd < 2.2-2
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
Requires:	libcap-ng-devel

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

%package -n golang-audit
Summary:	Go language interface to libaudit library
Summary(pl.UTF-8):	Interfejs języka Go do biblioteki libaudit
License:	LGPL v2.1+
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
%if %{with gccgo}
Requires:	gcc-go >= 5.1
%else
Requires:	golang >= 1.4
%endif

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
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch7 -p1

%if %{with flex_array_fix}
# workaround flexible array member (char buf[]) incompatible with swig<=4.1.1
cp /usr/include/linux/audit.h lib
%patch8 -p1
%endif

%if %{without python}
sed 's#[^ ]*swig/[^ ]*/Makefile ##g' -i configure.ac
sed 's/swig//' -i bindings/Makefile.am
%endif

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CC_FOR_BUILD="%{__cc}" \
	CPPFLAGS_FOR_BUILD="%{rpmcppflags}" \
	CFLAGS_FOR_BUILD="%{rpmcflags}" \
	LDFLAGS_FOR_BUILD="%{rpmldflags}" \
	%{?with_kerberos5:--enable-gssapi-krb5} \
	--enable-systemd \
	--with-apparmor \
	--with-io_uring \
	--with-libwrap \
	%{!?with_zos_remote:--disable-zos-remote}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/audit/rules.d,%{_var}/log/audit}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with flex_array_fix}
# undo include change
cd $RPM_BUILD_ROOT
patch -p0 --no-backup-if-mismatch < %{PATCH9}
cd -
%endif

# default to no audit (and no overhead)
cp -p rules/10-no-audit.rules $RPM_BUILD_ROOT%{_sysconfdir}/audit/rules.d

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/auditd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/auditd

install -d $RPM_BUILD_ROOT/%{_lib}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libaudit.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libaudit.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libaudit.so
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libauparse.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libauparse.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libauparse.so

# RH initscripts-specific
%{__rm} -r $RPM_BUILD_ROOT%{_libexecdir}/initscripts

%if %{with python2}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la
%endif

%if %{with python3}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
# Copy default rules into place on new installation
if [ ! -e %{_sysconfdir}/audit/audit.rules ] ; then
	cp -a %{_sysconfdir}/audit/rules.d/10-no-audit.rules %{_sysconfdir}/audit/audit.rules
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

%triggerpostun -- audit < 3.0
if [ -f %{_sysconfdir}/audisp/audisp-remote.conf.rpmsave -a ! -f %{_sysconfdir}/audit/audisp-remote.conf.rpmnew ]; then
	mv -f %{_sysconfdir}/audit/audisp-remote.conf %{_sysconfdir}/audit/audisp-remote.conf.rpmnew
	mv -f %{_sysconfdir}/audisp/audisp-remote.conf.rpmsave %{_sysconfdir}/audit/audisp-remote.conf
fi
if [ -f %{_sysconfdir}/audisp/plugins.d/af_unix.conf.rpmsave -a ! -f %{_sysconfdir}/audit/plugins.d/af_unix.conf.rpmnew ]; then
	mv -f %{_sysconfdir}/audit/plugins.d/af_unix.conf %{_sysconfdir}/audit/plugins.d/af_unix.conf.rpmnew
	mv -f %{_sysconfdir}/audisp/plugins.d/af_unix.conf.rpmsave %{_sysconfdir}/audit/plugins.d/af_unix.conf
fi
if [ -f %{_sysconfdir}/audisp/plugins.d/au-remote.conf.rpmsave -a ! -f %{_sysconfdir}/audit/plugins.d/au-remote.conf.rpmnew ]; then
	mv -f %{_sysconfdir}/audit/plugins.d/au-remote.conf %{_sysconfdir}/audit/plugins.d/au-remote.conf.rpmnew
	mv -f %{_sysconfdir}/audisp/plugins.d/au-remote.conf.rpmsave %{_sysconfdir}/audit/plugins.d/au-remote.conf
fi
if [ -f %{_sysconfdir}/audisp/plugins.d/syslog.conf.rpmsave -a ! -f %{_sysconfdir}/audit/plugins.d/syslog.conf.rpmnew ]; then
	mv -f %{_sysconfdir}/audit/plugins.d/syslog.conf %{_sysconfdir}/audit/plugins.d/syslog.conf.rpmnew
	mv -f %{_sysconfdir}/audisp/plugins.d/syslog.conf.rpmsave %{_sysconfdir}/audit/plugins.d/syslog.conf
fi
%if %{with zos_remote}
if [ -f %{_sysconfdir}/audisp/zos-remote.conf.rpmsave -a ! -f %{_sysconfdir}/audit/zos-remote.conf.rpmnew ]; then
	mv -f %{_sysconfdir}/audit/zos-remote.conf %{_sysconfdir}/audit/zos-remote.conf.rpmnew
	mv -f %{_sysconfdir}/audisp/zos-remote.conf.rpmsave %{_sysconfdir}/audit/zos-remote.conf
fi
if [ -f %{_sysconfdir}/audisp/plugins.d/audisp-zos-remote.conf.rpmsave -a ! -f %{_sysconfdir}/audit/plugins.d/audisp-zos-remote.conf.rpmnew ]; then
	mv -f %{_sysconfdir}/audit/plugins.d/audisp-zos-remote.conf %{_sysconfdir}/audit/plugins.d/audisp-zos-remote.conf.rpmnew
	mv -f %{_sysconfdir}/audisp/plugins.d/audisp-zos-remote.conf.rpmsave %{_sysconfdir}/audit/plugins.d/audisp-zos-remote.conf
fi
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS rules/{README-rules,*.rules} init.d/auditd.cron
%attr(750,root,root) %{_bindir}/aulast
%attr(750,root,root) %{_bindir}/aulastlog
%attr(750,root,root) %{_bindir}/ausyscall
%attr(750,root,root) %{_bindir}/auvirt
%attr(750,root,root) %{_sbindir}/auditctl
%attr(750,root,root) %{_sbindir}/auditd
%attr(750,root,root) %{_sbindir}/augenrules
%attr(750,root,root) %{_sbindir}/aureport
%attr(750,root,root) %{_sbindir}/ausearch
%attr(750,root,root) %{_sbindir}/autrace
%attr(755,root,root) %{_sbindir}/audisp-af_unix
%attr(755,root,root) %{_sbindir}/audisp-remote
%attr(755,root,root) %{_sbindir}/audisp-syslog
%{_libexecdir}/audit-functions
%dir %{_datadir}/audit
%{_datadir}/audit/sample-rules
%dir %{_sysconfdir}/audit
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/audisp-remote.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/audit-stop.rules
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/auditd.conf
%dir %{_sysconfdir}/audit/plugins.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/plugins.d/af_unix.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/plugins.d/au-remote.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/plugins.d/syslog.conf
%dir %{_sysconfdir}/audit/rules.d
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/audit/rules.d/10-no-audit.rules
%attr(754,root,root) /etc/rc.d/init.d/auditd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/auditd
%{systemdunitdir}/auditd.service
%attr(750,root,root) %dir %{_var}/log/audit
%{_mandir}/man5/audisp-remote.conf.5*
%{_mandir}/man5/auditd.conf.5*
%{_mandir}/man5/auditd-plugins.5*
%{_mandir}/man5/ausearch-expression.5*
%{_mandir}/man7/audit.rules.7*
%{_mandir}/man8/audisp-af_unix.8*
%{_mandir}/man8/audisp-remote.8*
%{_mandir}/man8/audisp-syslog.8*
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

%if %{with zos_remote}
%attr(755,root,root) %{_sbindir}/audispd-zos-remote
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/zos-remote.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/plugins.d/audispd-zos-remote.conf
%{_mandir}/man5/zos-remote.conf.5*
%{_mandir}/man8/audispd-zos-remote.8*
%endif

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
%{_aclocaldir}/audit.m4
%{_mandir}/man3/audit_*.3*
%{_mandir}/man3/auparse_*.3*
%{_mandir}/man3/ausearch_*.3*
%{_mandir}/man3/get_auditfail_action.3*
%{_mandir}/man3/set_aumessage_mode.3*

%files libs-static
%defattr(644,root,root,755)
%{_libdir}/libaudit.a
%{_libdir}/libauparse.a

%if %{with golang}
%files -n golang-audit
%defattr(644,root,root,755)
%dir %{_libdir}/golang/src/redhat.com
%{_libdir}/golang/src/redhat.com/audit
%endif

%if %{with python2}
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
%{py3_sitedir}/__pycache__/audit.cpython-*.py[co]
%endif

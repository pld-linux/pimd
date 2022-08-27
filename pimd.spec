Summary:	Multicast routing daemon
Summary(pl.UTF-8):	Demon routingu multicastowego
Name:		pimd
Version:	2.3.2
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.troglobit.com/pimd/%{name}-%{version}.tar.gz
# Source0-md5:	a3c03e40540980b2c06e265a17988e60
Source1:	%{name}.init
URL:		https://troglobit.com/projects/pimd/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pimd is a lightweight, stand-alone PIM-Sparse Mode implementation that
may be freely distributed or deployed. pimd implements the full PIM-SM
specification (RFC 2362) with a few noted exceptions.

%description -l pl.UTF-8
pimd jest niewielką, samodzielną implementacją PIM-Sparse Mode. pimd
ma zaimplementowaną pełną specyfikację PIM-SM (RFC 2362) z kilkoma
wyjątkami.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir}

export CPPFLAGS="%{rpmcppflags}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"
%{__make} \
	CC="%{__cc}" \
	mandir="%{_mandir}/man8"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pimd

%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/share/doc/pimd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pimd
%service pimd restart

%preun
if [ "$1" = "0" ]; then
	%service pimd stop
	/sbin/chkconfig --del pimd >&2
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog.org CODE-OF-CONDUCT.md CONTRIBUTING.md CREDITS FAQ.md LICENSE* README{,-config,-debug}.md TODO.org
%lang(jp) %doc README.config.jp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pimd.conf
%attr(755,root,root) %{_sbindir}/pimd
%attr(754,root,root) /etc/rc.d/init.d/*
%{_mandir}/man8/pimd.8*

%define	ver_a 2.1.0
%define	ver_b alpha28
Summary:	Multicast routing daemon
Summary(pl):	Demon routingu multicastowego
Name:		pimd
Version:	%{ver_a}_%{ver_b}
Release:	2
License:	custom
Group:		Networking/Daemons
Source0:	http://catarina.usc.edu/pim/pimd/%{name}-%{ver_a}-%{ver_b}.tar.gz
# Source0-md5:	05a0f591434b8ed0051132112159a59f
Source1:	%{name}.init
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-time.patch
URL:		http://catarina.usc.edu/pim/
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pimd is a lightweight, stand-alone PIM-Sparse Mode implementation that
may be freely distributed or deployed. pimd implements the full PIM-SM
specification (RFC 2362) with a few noted exceptions.

%description -l pl
pimd jest niewielk±, samodzieln± implementacj± PIM-Sparse Mode. pimd
ma zaimplementowan± pe³n± specyfikacjê PIM-SM (RFC 2362) z kilkoma
wyj±tkami.

%prep
%setup -q -n %{name}-%{ver_a}-%{ver_b}
%patch0 -p1
%patch1 -p1

# these files are outdated (conflicting with current glibc)
rm -f include/linux/netinet/in*

%build
%{__make} \
	CC="%{__cc} %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sbindir},%{_mandir}/man8}

install pimd $RPM_BUILD_ROOT%{_sbindir}
install pimd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pimd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pimd
if [ -f /var/lock/subsys/pimd ]; then
	/etc/rc.d/init.d/pimd restart >&2
else
	echo "Run '/etc/rc.d/init.d/pimd start' to start routing deamon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/pimd ]; then
		/etc/rc.d/init.d/pimd stop >&2
	fi
	/sbin/chkconfig --del pimd >&2
fi

%files
%defattr(644,root,root,755)
%doc README LICENSE* RELEASE.NOTES CHANGES BUGS.TODO
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pimd.conf

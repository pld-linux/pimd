%define	ver_a 2.1.0
%define	ver_b alpha28
Summary:	Multicast routing daemon
Name:		pimd
Version:	%{ver_a}_%{ver_b}
Release:	1
License:	Custom
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	http://catarina.usc.edu/pim/pimd/%{name}-%{ver_a}-%{ver_b}.tar.gz
Source1:	%{name}.init	
Patch0:		pimd-Makefile.patch
Prereq:		/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pimd is a lightweight, stand-alone PIM-Sparse Mode implementation that
may be freely distributed or deployed. pimd implements the full PIM-SM
specification (RFC 2362) with a few noted exceptions.

%prep
%setup -q -n %{name}-%{ver_a}-%{ver_b}
%patch0 -p1

%build
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/rc.d/init.d,%{_sbindir},%{_mandir}/man8}

install pimd $RPM_BUILD_ROOT%{_sbindir}
install pimd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/pimd

gzip -9nf README LICENSE* RELEASE.NOTES CHANGES BUGS.TODO 

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pimd.conf

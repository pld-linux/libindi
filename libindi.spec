Summary:	Instrument Neutral Distributed Interface
Name:		indilib
Version:	0.5
Release:	3
License:	LGPL
Group:		Libraries
URL:		http://indi.sourceforge.net/
Source0:	http://dl.sourceforge.net/indi/%{name}-%{version}.tar.gz
# Source0-md5:	1b370b2aad7c6aa79faccbec20b30278
Patch0:		%{name}-gcc-4.3.patch
BuildRequires:	cfitsio-devel
BuildRequires:	libnova-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
INDI is a distributed control protocol designed to operate
astronomical instrumentation. INDI is small, flexible, easy to parse,
and scalable. It supports common DCS functions such as remote control,
data acquisition, monitoring, and a lot more.

With INDI, you have a total transparent control over your instruments
so you can get more science with less time.

%package devel
Summary:	Header files and static libraries from indilib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Libraries and includes files for developing programs based on indilib.

%package static
Summary:	Static indilib library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static indilib library.

%prep
%setup -q -n indi
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING.LIB ChangeLog NEWS README* TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libsbigudrv.so.*
%dir %{_datadir}/indi
%{_datadir}/indi/apogee_caminfo.xml

%files devel
%defattr(644,root,root,755)
%{_libdir}/libsbigudrv.la
%attr(755,root,root) %{_libdir}/libsbigudrv.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libsbigudrv.a

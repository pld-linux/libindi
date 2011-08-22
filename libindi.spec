Summary:	Instrument Neutral Distributed Interface
Summary(pl.UTF-8):	Instrument Neutral Distributed Interface - interfejs do sterowania przyrządami
Name:		libindi
Version:	0.8
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/indi/%{name}_%{version}.tar.gz
# Source0-md5:	ca2b7c56431eb5e08218929e5eb72150
Patch0:		%{name}-build.patch
URL:		http://www.indilib.org/
BuildRequires:	cfitsio-devel >= 3.03
BuildRequires:	cmake >= 2.8.0
# not actually used now
#BuildRequires:	libfli-devel >= 1.7
BuildRequires:	libnova-devel >= 0.12.2
BuildRequires:	libusb-compat-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.603
BuildRequires:	zlib-devel
Requires:	cfitsio >= 3.03
Requires:	libnova >= 0.12.2
Obsoletes:	indilib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
INDI is a distributed control protocol designed to operate
astronomical instrumentation. INDI is small, flexible, easy to parse,
and scalable. It supports common DCS functions such as remote control,
data acquisition, monitoring, and a lot more.

With INDI, you have a total transparent control over your instruments
so you can get more science with less time.

%description -l pl.UTF-8
INDI to rozproszony protokół sterujący zaprojektowany do operowania
przyrządami astronomicznymi. Jest mały, elastyczny, łatwy do
analizowania i skalowalny. Obsługuje popularne funkcje DCS, takie jak
zdalne sterowanie, zbieranie danych, monitorowanie i inne.

INDO zapewnia całkowicie przezroczyste sterowanie przyrządami,
pozostawiając więcej czasu na cele naukowe.

%package devel
Summary:	Header files for INDI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki INDI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	indilib-devel

%description devel
Header files for INDI library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki INDI.

%package static
Summary:	Static INDI library
Summary(pl.UTF-8):	Statyczna biblioteka INDI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	indilib-static

%description static
Static INDI library.

%description static -l pl.UTF-8
Statyczna biblioteka INDI.

%prep
%setup -q
%undos CMakeLists.txt
%patch0 -p1

%build
install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README* TODO
%attr(755,root,root) %{_bindir}/indi_celestron_gps
%attr(755,root,root) %{_bindir}/indi_eval
%attr(755,root,root) %{_bindir}/indi_getprop
%attr(755,root,root) %{_bindir}/indi_intelliscope
%attr(755,root,root) %{_bindir}/indi_lx200basic
%attr(755,root,root) %{_bindir}/indi_lx200generic
%attr(755,root,root) %{_bindir}/indi_meade_lpi
%attr(755,root,root) %{_bindir}/indi_orion_atlas
%attr(755,root,root) %{_bindir}/indi_robo_focus
%attr(755,root,root) %{_bindir}/indi_sbig_stv
%attr(755,root,root) %{_bindir}/indi_setprop
%attr(755,root,root) %{_bindir}/indi_simulator_ccd
%attr(755,root,root) %{_bindir}/indi_simulator_telescope
%attr(755,root,root) %{_bindir}/indi_simulator_wheel
%attr(755,root,root) %{_bindir}/indi_skycommander
%attr(755,root,root) %{_bindir}/indi_synscan
%attr(755,root,root) %{_bindir}/indi_tcfs_focus
%attr(755,root,root) %{_bindir}/indi_temma
%attr(755,root,root) %{_bindir}/indi_trutech_wheel
%attr(755,root,root) %{_bindir}/indi_v4l_generic
%attr(755,root,root) %{_bindir}/indi_v4l_philips
%attr(755,root,root) %{_bindir}/indiserver
%attr(755,root,root) %{_libdir}/libindi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindi.so.0
%dir %{_datadir}/indi
%{_datadir}/indi/drivers.xml
%{_datadir}/indi/indi_tcfs_sk.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libindi.so
%{_includedir}/libindi
%{_pkgconfigdir}/libindi.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libindiclient.a
%{_libdir}/libindidriver.a
%{_libdir}/libindimain.a

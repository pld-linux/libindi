Summary:	Instrument Neutral Distributed Interface
Summary(pl.UTF-8):	Instrument Neutral Distributed Interface - interfejs do sterowania przyrządami
Name:		libindi
Version:	0.9.7
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/indi/%{name}_%{version}.tar.gz
# Source0-md5:	3e457c4226d7a445a0d89c044cced6b7
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

# these libs rely on symbols in drivers/binaries
%define		skip_post_check_so	libindidriver.so.* libindimain.so.*

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
Summary:	Header files for INDI libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek INDI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	indilib-devel
Obsoletes:	libindi-static

%description devel
Header files for INDI libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek INDI.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake \
%if "%{_lib}" == "lib64"
	-DLIB_POSTFIX=64 \
%endif
	..

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
%attr(755,root,root) %{_bindir}/indi_gpusb
%attr(755,root,root) %{_bindir}/indi_ieq45_8406
%attr(755,root,root) %{_bindir}/indi_ieq45_8407
%attr(755,root,root) %{_bindir}/indi_intelliscope
%attr(755,root,root) %{_bindir}/indi_joystick
%attr(755,root,root) %{_bindir}/indi_lx200_16
%attr(755,root,root) %{_bindir}/indi_lx200ap
%attr(755,root,root) %{_bindir}/indi_lx200autostar
%attr(755,root,root) %{_bindir}/indi_lx200basic
%attr(755,root,root) %{_bindir}/indi_lx200classic
%attr(755,root,root) %{_bindir}/indi_lx200fs2
%attr(755,root,root) %{_bindir}/indi_lx200generic
%attr(755,root,root) %{_bindir}/indi_lx200genericlegacy
%attr(755,root,root) %{_bindir}/indi_lx200gps
%attr(755,root,root) %{_bindir}/indi_magellan1
%attr(755,root,root) %{_bindir}/indi_meade_lpi
%attr(755,root,root) %{_bindir}/indi_robo_focus
%attr(755,root,root) %{_bindir}/indi_sbig_stv
%attr(755,root,root) %{_bindir}/indi_setprop
%attr(755,root,root) %{_bindir}/indi_simulator_ccd
%attr(755,root,root) %{_bindir}/indi_simulator_focus
%attr(755,root,root) %{_bindir}/indi_simulator_telescope
%attr(755,root,root) %{_bindir}/indi_simulator_wheel
%attr(755,root,root) %{_bindir}/indi_skycommander
%attr(755,root,root) %{_bindir}/indi_synscan
%attr(755,root,root) %{_bindir}/indi_tcfs_focus
%attr(755,root,root) %{_bindir}/indi_tcfs3_focus
%attr(755,root,root) %{_bindir}/indi_temma
%attr(755,root,root) %{_bindir}/indi_trutech_wheel
%attr(755,root,root) %{_bindir}/indi_v4l_generic
%attr(755,root,root) %{_bindir}/indi_v4l_philips
%attr(755,root,root) %{_bindir}/indiserver
%attr(755,root,root) %{_libdir}/libindi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindi.so.0
%attr(755,root,root) %{_libdir}/libindidriver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindidriver.so.0
%attr(755,root,root) %{_libdir}/libindimain.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindimain.so.0
%dir %{_datadir}/indi
%{_datadir}/indi/drivers.xml
%{_datadir}/indi/indi_tcfs_sk.xml
/lib/udev/rules.d/99-gpusb.rules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libindi.so
%attr(755,root,root) %{_libdir}/libindidriver.so
%attr(755,root,root) %{_libdir}/libindimain.so
%{_libdir}/libindiclient.a
%{_includedir}/libindi
%{_pkgconfigdir}/libindi.pc

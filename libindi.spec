#
# Conditional build:
%bcond_without	qt5	# Qt5 client library
#
Summary:	Instrument Neutral Distributed Interface
Summary(pl.UTF-8):	Instrument Neutral Distributed Interface - interfejs do sterowania przyrządami
Name:		libindi
Version:	1.9.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://github.com/indilib/indi/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	32524aca0ea53a6f224468fae6107edf
Patch0:		no_static_lib.patch
Patch1:		link.patch
URL:		http://www.indilib.org/
%{?with_qt5:BuildRequires:	Qt5Network-devel >= 5.0}
BuildRequires:	cfitsio-devel >= 3.03
BuildRequires:	cmake >= 3.0
BuildRequires:	curl-devel
BuildRequires:	gsl-devel >= 1.10
# not actually used now
#BuildRequires:	libfli-devel >= 1.7
BuildRequires:	libjpeg-devel
BuildRequires:	libnova-devel >= 0.12.2
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	libtheora-devel
BuildRequires:	libusb-devel >= 1
BuildRequires:	pkgconfig
%{?with_qt5:BuildRequires:	qt5-build >= 5.0}
BuildRequires:	rpmbuild(macros) >= 1.603
BuildRequires:	zlib-devel
Requires:	cfitsio >= 3.03
Requires:	gsl >= 1.10
Requires:	libnova >= 0.12.2
Obsoletes:	indilib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# these libs rely on symbols in drivers/binaries
%define		skip_post_check_so	libindidriver.so.* libindiAlignmentDriver.so.*

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

%description devel
Header files for INDI libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek INDI.

%package static
Summary:	Static INDI libraries
Summary(pl.UTF-8):	Statyczne biblioteki INDI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static INDI libraries.

%description static -l pl.UTF-8
Statyczne biblioteki INDI.

%package qt5-devel
Summary:	INDI Qt5 client library
Summary(pl.UTF-8):	Biblioteka kliencka INDI oparta o Qt5
Group:		Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	Qt5Network-devel >= 5

%description qt5-devel
INDI Qt5 client library.

%description qt5-devel -l pl.UTF-8
Biblioteka kliencka INDI oparta o Qt5.

%prep
%setup -q -n indi-%{version}
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
# note: CMakeLists expect relative CMAKE_INSTALL_LIBDIR
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{?with_qt5:-DINDI_BUILD_QT5_CLIENT=ON} \
	-DINDI_MATH_PLUGINS_DIRECTORY:PATH=%{_libdir}/indi/MathPlugins

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
%doc AUTHORS ChangeLog NEWS README*
%attr(755,root,root) %{_bindir}/indi_aaf2_focus
%attr(755,root,root) %{_bindir}/indi_activefocuser_focus
%attr(755,root,root) %{_bindir}/indi_arduinost4
%attr(755,root,root) %{_bindir}/indi_astromech_lpm
%attr(755,root,root) %{_bindir}/indi_astrometry
%attr(755,root,root) %{_bindir}/indi_astrotrac_telescope
%attr(755,root,root) %{_bindir}/indi_baader_dome
%attr(755,root,root) %{_bindir}/indi_celestron_gps
%attr(755,root,root) %{_bindir}/indi_celestron_sct_focus
%attr(755,root,root) %{_bindir}/indi_crux_mount
%attr(755,root,root) %{_bindir}/indi_ddw_dome
%attr(755,root,root) %{_bindir}/indi_deepskydad_af1_focus
%attr(755,root,root) %{_bindir}/indi_deepskydad_af2_focus
%attr(755,root,root) %{_bindir}/indi_deepskydad_af3_focus
%attr(755,root,root) %{_bindir}/indi_deepskydad_fp1
%attr(755,root,root) %{_bindir}/indi_deepskydad_fr1
%attr(755,root,root) %{_bindir}/indi_dmfc_focus
%attr(755,root,root) %{_bindir}/indi_domepro2_dome
%attr(755,root,root) %{_bindir}/indi_dsc_telescope
%attr(755,root,root) %{_bindir}/indi_efa_focus
%attr(755,root,root) %{_bindir}/indi_eq500x_telescope
%attr(755,root,root) %{_bindir}/indi_eval
%attr(755,root,root) %{_bindir}/indi_falcon_rotator
%attr(755,root,root) %{_bindir}/indi_fcusb_focus
%attr(755,root,root) %{_bindir}/indi_flipflat
%attr(755,root,root) %{_bindir}/indi_gemini_focus
%attr(755,root,root) %{_bindir}/indi_getprop
%attr(755,root,root) %{_bindir}/indi_gpusb
%attr(755,root,root) %{_bindir}/indi_hid_test
%attr(755,root,root) %{_bindir}/indi_hitecastrodc_focus
%attr(755,root,root) %{_bindir}/indi_ieqlegacy_telescope
%attr(755,root,root) %{_bindir}/indi_ieq_telescope
%attr(755,root,root) %{_bindir}/indi_imager_agent
%attr(755,root,root) %{_bindir}/indi_integra_focus
%attr(755,root,root) %{_bindir}/indi_ioptronHC8406
%attr(755,root,root) %{_bindir}/indi_ioptronv3_telescope
%attr(755,root,root) %{_bindir}/indi_joystick
%attr(755,root,root) %{_bindir}/indi_lacerta_mfoc_focus
%attr(755,root,root) %{_bindir}/indi_lakeside_focus
%attr(755,root,root) %{_bindir}/indi_lx200_10micron
%attr(755,root,root) %{_bindir}/indi_lx200_16
%attr(755,root,root) %{_bindir}/indi_lx200ap
%attr(755,root,root) %{_bindir}/indi_lx200ap_experimental
%attr(755,root,root) %{_bindir}/indi_lx200ap_gtocp2
%attr(755,root,root) %{_bindir}/indi_lx200autostar
%attr(755,root,root) %{_bindir}/indi_lx200basic
%attr(755,root,root) %{_bindir}/indi_lx200classic
%attr(755,root,root) %{_bindir}/indi_lx200fs2
%attr(755,root,root) %{_bindir}/indi_lx200gemini
%attr(755,root,root) %{_bindir}/indi_lx200generic
%attr(755,root,root) %{_bindir}/indi_lx200gotonova
%attr(755,root,root) %{_bindir}/indi_lx200gps
%attr(755,root,root) %{_bindir}/indi_lx200_OnStep
%attr(755,root,root) %{_bindir}/indi_lx200pulsar2
%attr(755,root,root) %{_bindir}/indi_lx200ss2000pc
%attr(755,root,root) %{_bindir}/indi_lx200_TeenAstro
%attr(755,root,root) %{_bindir}/indi_lx200zeq25
%attr(755,root,root) %{_bindir}/indi_lynx_focus
%attr(755,root,root) %{_bindir}/indi_manual_wheel
%attr(755,root,root) %{_bindir}/indi_mbox_weather
%attr(755,root,root) %{_bindir}/indi_meta_weather
%attr(755,root,root) %{_bindir}/indi_microtouch_focus
%attr(755,root,root) %{_bindir}/indi_moonlitedro_focus
%attr(755,root,root) %{_bindir}/indi_moonlite_focus
%attr(755,root,root) %{_bindir}/indi_myfocuserpro2_focus
%attr(755,root,root) %{_bindir}/indi_nfocus
%attr(755,root,root) %{_bindir}/indi_nightcrawler_focus
%attr(755,root,root) %{_bindir}/indi_nstep_focus
%attr(755,root,root) %{_bindir}/indi_onfocus_focus
%attr(755,root,root) %{_bindir}/indi_openweathermap_weather
%attr(755,root,root) %{_bindir}/indi_optec_wheel
%attr(755,root,root) %{_bindir}/indi_paramount_telescope
%attr(755,root,root) %{_bindir}/indi_pegasus_flatmaster
%attr(755,root,root) %{_bindir}/indi_pegasus_focuscube
%attr(755,root,root) %{_bindir}/indi_pegasus_ppb
%attr(755,root,root) %{_bindir}/indi_pegasus_ppba
%attr(755,root,root) %{_bindir}/indi_pegasus_scopsoag
%attr(755,root,root) %{_bindir}/indi_pegasus_uch
%attr(755,root,root) %{_bindir}/indi_pegasus_upb
%attr(755,root,root) %{_bindir}/indi_perfectstar_focus
%attr(755,root,root) %{_bindir}/indi_planewave_deltat
%attr(755,root,root) %{_bindir}/indi_pmc8_telescope
%attr(755,root,root) %{_bindir}/indi_pyxis_rotator
%attr(755,root,root) %{_bindir}/indi_qhycfw1_wheel
%attr(755,root,root) %{_bindir}/indi_qhycfw2_wheel
%attr(755,root,root) %{_bindir}/indi_qhycfw3_wheel
%attr(755,root,root) %{_bindir}/indi_quantum_wheel
%attr(755,root,root) %{_bindir}/indi_rainbowrsf_focus
%attr(755,root,root) %{_bindir}/indi_rainbow_telescope
%attr(755,root,root) %{_bindir}/indi_rbfocus_focus
%attr(755,root,root) %{_bindir}/indi_rigel_dome
%attr(755,root,root) %{_bindir}/indi_robo_focus
%attr(755,root,root) %{_bindir}/indi_rolloff_dome
%attr(755,root,root) %{_bindir}/indi_rtlsdr
%attr(755,root,root) %{_bindir}/indi_scopedome_dome
%attr(755,root,root) %{_bindir}/indi_script_dome
%attr(755,root,root) %{_bindir}/indi_script_telescope
%attr(755,root,root) %{_bindir}/indiserver
%attr(755,root,root) %{_bindir}/indi_sestosenso2_focus
%attr(755,root,root) %{_bindir}/indi_sestosenso_focus
%attr(755,root,root) %{_bindir}/indi_setprop
%attr(755,root,root) %{_bindir}/indi_siefs_focus
%attr(755,root,root) %{_bindir}/indi_simulator_ccd
%attr(755,root,root) %{_bindir}/indi_simulator_dome
%attr(755,root,root) %{_bindir}/indi_simulator_focus
%attr(755,root,root) %{_bindir}/indi_simulator_gps
%attr(755,root,root) %{_bindir}/indi_simulator_guide
%attr(755,root,root) %{_bindir}/indi_simulator_lightpanel
%attr(755,root,root) %{_bindir}/indi_simulator_receiver
%attr(755,root,root) %{_bindir}/indi_simulator_rotator
%attr(755,root,root) %{_bindir}/indi_simulator_sqm
%attr(755,root,root) %{_bindir}/indi_simulator_telescope
%attr(755,root,root) %{_bindir}/indi_simulator_weather
%attr(755,root,root) %{_bindir}/indi_simulator_wheel
%attr(755,root,root) %{_bindir}/indi_skycommander_telescope
%attr(755,root,root) %{_bindir}/indi_skysafari
%attr(755,root,root) %{_bindir}/indi_skywatcherAltAzMount
%attr(755,root,root) %{_bindir}/indi_skywatcherAltAzSimple
%attr(755,root,root) %{_bindir}/indi_smartfocus_focus
%attr(755,root,root) %{_bindir}/indi_snapcap
%attr(755,root,root) %{_bindir}/indi_sqm_weather
%attr(755,root,root) %{_bindir}/indi_star2000
%attr(755,root,root) %{_bindir}/indi_steeldrive2_focus
%attr(755,root,root) %{_bindir}/indi_steeldrive_focus
%attr(755,root,root) %{_bindir}/indi_synscanlegacy_telescope
%attr(755,root,root) %{_bindir}/indi_synscan_telescope
%attr(755,root,root) %{_bindir}/indi_tcfs3_focus
%attr(755,root,root) %{_bindir}/indi_tcfs_focus
%attr(755,root,root) %{_bindir}/indi_teenastro_focus
%attr(755,root,root) %{_bindir}/indi_temma_telescope
%attr(755,root,root) %{_bindir}/indi_trutech_wheel
%attr(755,root,root) %{_bindir}/indi_usbdewpoint
%attr(755,root,root) %{_bindir}/indi_usbfocusv3_focus
%attr(755,root,root) %{_bindir}/indi_v4l2_ccd
%attr(755,root,root) %{_bindir}/indi_vantage_weather
%attr(755,root,root) %{_bindir}/indi_watchdog
%attr(755,root,root) %{_bindir}/indi_watcher_weather
%attr(755,root,root) %{_bindir}/indi_weather_safety_proxy
%attr(755,root,root) %{_bindir}/indi_xagyl_wheel
%attr(755,root,root) %{_libdir}/libindidriver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindidriver.so.1
%attr(755,root,root) %{_libdir}/libindilx200.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindilx200.so.1
%attr(755,root,root) %{_libdir}/libindiAlignmentDriver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindiAlignmentDriver.so.1
%dir %{_libdir}/indi
%dir %{_libdir}/indi/MathPlugins
%attr(755,root,root) %{_libdir}/indi/MathPlugins/libindi_Nearest_MathPlugin.so
%attr(755,root,root) %{_libdir}/indi/MathPlugins/libindi_SVD_MathPlugin.so
%dir %{_datadir}/indi
%{_datadir}/indi/drivers.xml
%{_datadir}/indi/indi_tcfs_sk.xml
/lib/udev/rules.d/80-dbk21-camera.rules
/lib/udev/rules.d/99-indi_auxiliary.rules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libindidriver.so
%attr(755,root,root) %{_libdir}/libindilx200.so
%attr(755,root,root) %{_libdir}/libindiAlignmentDriver.so
%{_libdir}/libindiAlignmentClient.a
%{_libdir}/libindiclient.a
%{_includedir}/libindi
%{?with_qt5:%exclude %{_includedir}/libindi/baseclientqt.h}
%{_pkgconfigdir}/libindi.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libindidriver.a

%if %{with qt5}
%files qt5-devel
%defattr(644,root,root,755)
%{_libdir}/libindiclientqt.a
%{_includedir}/libindi/baseclientqt.h
%endif

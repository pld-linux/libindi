#
# Conditional build:
%bcond_without	qt5		# Qt5 client library
%bcond_without	websocketpp	# websocket support (via websocketpp)
#
Summary:	Instrument Neutral Distributed Interface
Summary(pl.UTF-8):	Instrument Neutral Distributed Interface - interfejs do sterowania przyrządami
Name:		libindi
Version:	2.1.2.1
Release:	2
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/indilib/indi/releases
Source0:	https://github.com/indilib/indi/archive/v%{version}/indi-%{version}.tar.gz
# Source0-md5:	64d6761e15c5f700e39397f54641bf8a
Patch0:		no_static_lib.patch
Patch1:		link.patch
URL:		https://www.indilib.org/
%{?with_qt5:BuildRequires:	Qt5Core-devel >= 5.0}
%{?with_qt5:BuildRequires:	Qt5Network-devel >= 5.0}
%{?with_websocketpp:BuildRequires:	boost-devel}
BuildRequires:	cfitsio-devel >= 3.03
BuildRequires:	cmake >= 3.13
BuildRequires:	cpp-httplib-devel
BuildRequires:	curl-devel
BuildRequires:	fftw3-devel >= 3
BuildRequires:	gsl-devel >= 1.10
BuildRequires:	libev-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libogg-devel
BuildRequires:	libnova-devel >= 0.12.2
BuildRequires:	librtlsdr-devel
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	libtheora-devel
BuildRequires:	libusb-devel >= 1
BuildRequires:	libxisf-devel
BuildRequires:	nlohmann-json-devel
BuildRequires:	pkgconfig
%{?with_qt5:BuildRequires:	qt5-build >= 5.0}
BuildRequires:	rpmbuild(macros) >= 1.603
%{?with_websocketpp:BuildRequires:	websocketpp-devel}
BuildRequires:	zlib-devel
Requires:	cfitsio >= 3.03
Requires:	gsl >= 1.10
Requires:	libnova >= 0.12.2
Obsoletes:	indilib < 0.6
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
Summary:	Header files for INDI libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek INDI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	indilib-devel < 0.6

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

%package qt5
Summary:	INDI Qt5 client library
Summary(pl.UTF-8):	Biblioteka kliencka INDI oparta na Qt5
Group:		Libraries
Requires:	Qt5Network >= 5
Requires:	libnova >= 0.12.2

%description qt5
INDI Qt5 client library.

%description qt5 -l pl.UTF-8
Biblioteka kliencka INDI oparta na Qt5.

%package qt5-devel
Summary:	Header file for INDI Qt5 client library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki klienckiej INDI opartej na Qt5
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	Qt5Network-devel >= 5

%description qt5-devel
Header file for INDI Qt5 client library.

%description qt5-devel -l pl.UTF-8
Plik nagłówkowy biblioteki klienckiej INDI opartej na Qt5.

%package qt5-static
Summary:	Static INDI Qt5 client library
Summary(pl.UTF-8):	Statyczna biblioteka kliencka INDI oparta na Qt5
Group:		Development/Libraries
Requires:	%{name}-qt5-devel = %{version}-%{release}

%description qt5-static
Static INDI Qt5 client library.

%description qt5-static -l pl.UTF-8
Statyczna biblioteka kliencka INDI oparta na Qt5.

%prep
%setup -q -n indi-%{version}
%patch -P0 -p1
%patch -P1 -p1

%build
# note: CMakeLists expect relative CMAKE_INSTALL_LIBDIR
%cmake -B build \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{?with_qt5:-DINDI_BUILD_QT5_CLIENT=ON} \
	%{?with_websocketpp:-DINDI_BUILD_WEBSOCKET=ON} \
	-DINDI_MATH_PLUGINS_DIRECTORY:PATH=%{_libdir}/indi/MathPlugins \
	-DINDI_SYSTEM_HTTPLIB=ON \
	-DINDI_SYSTEM_JSONLIB=ON

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	qt5 -p /sbin/ldconfig
%postun qt5 -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING.BSD COPYRIGHT ChangeLog NEWS README README.md
%attr(755,root,root) %{_bindir}/indi_Excalibur
%attr(755,root,root) %{_bindir}/indi_aaf2_focus
%attr(755,root,root) %{_bindir}/indi_activefocuser_focus
%attr(755,root,root) %{_bindir}/indi_alluna_tcs2
%attr(755,root,root) %{_bindir}/indi_alto
%attr(755,root,root) %{_bindir}/indi_arduinost4
%attr(755,root,root) %{_bindir}/indi_astrolink4
%attr(755,root,root) %{_bindir}/indi_astrolink4mini2
%attr(755,root,root) %{_bindir}/indi_astromech_lpm
%attr(755,root,root) %{_bindir}/indi_astromechfoc
%attr(755,root,root) %{_bindir}/indi_astrometry
%attr(755,root,root) %{_bindir}/indi_astrotrac_telescope
%attr(755,root,root) %{_bindir}/indi_baader_dome
%attr(755,root,root) %{_bindir}/indi_celestron_gps
%attr(755,root,root) %{_bindir}/indi_celestron_sct_focus
%attr(755,root,root) %{_bindir}/indi_cheapodc
%attr(755,root,root) %{_bindir}/indi_crux_mount
%attr(755,root,root) %{_bindir}/indi_ddw_dome
%attr(755,root,root) %{_bindir}/indi_deepskydad_af1_focus
%attr(755,root,root) %{_bindir}/indi_deepskydad_af2_focus
%attr(755,root,root) %{_bindir}/indi_deepskydad_af3_focus
%attr(755,root,root) %{_bindir}/indi_deepskydad_fp
%attr(755,root,root) %{_bindir}/indi_deepskydad_fr1
%attr(755,root,root) %{_bindir}/indi_dmfc_focus
%attr(755,root,root) %{_bindir}/indi_domepro2_dome
%attr(755,root,root) %{_bindir}/indi_dragon_light
%attr(755,root,root) %{_bindir}/indi_dragonlair_dome
%attr(755,root,root) %{_bindir}/indi_dreamfocuser_focus
%attr(755,root,root) %{_bindir}/indi_dsc_telescope
%attr(755,root,root) %{_bindir}/indi_efa_focus
%attr(755,root,root) %{_bindir}/indi_eq500x_telescope
%attr(755,root,root) %{_bindir}/indi_esatto_focus
%attr(755,root,root) %{_bindir}/indi_esattoarco_focus
%attr(755,root,root) %{_bindir}/indi_eval
%attr(755,root,root) %{_bindir}/indi_falcon_rotator
%attr(755,root,root) %{_bindir}/indi_falconv2_rotator
%attr(755,root,root) %{_bindir}/indi_fcusb_focus
%attr(755,root,root) %{_bindir}/indi_flipflat
%attr(755,root,root) %{_bindir}/indi_gemini_focus
%attr(755,root,root) %{_bindir}/indi_getprop
%attr(755,root,root) %{_bindir}/indi_giotto
%attr(755,root,root) %{_bindir}/indi_gpusb
%attr(755,root,root) %{_bindir}/indi_hid_test
%attr(755,root,root) %{_bindir}/indi_hitecastrodc_focus
%attr(755,root,root) %{_bindir}/indi_ieaf_focus
%attr(755,root,root) %{_bindir}/indi_ieqlegacy_telescope
%attr(755,root,root) %{_bindir}/indi_ieq_telescope
%attr(755,root,root) %{_bindir}/indi_imager_agent
%attr(755,root,root) %{_bindir}/indi_integra_focus
%attr(755,root,root) %{_bindir}/indi_ioptronHC8406
%attr(755,root,root) %{_bindir}/indi_ioptron_wheel
%attr(755,root,root) %{_bindir}/indi_ioptronv3_telescope
%attr(755,root,root) %{_bindir}/indi_ipx800v4
%attr(755,root,root) %{_bindir}/indi_joystick
%attr(755,root,root) %{_bindir}/indi_lacerta_mfoc_fmc_focus
%attr(755,root,root) %{_bindir}/indi_lacerta_mfoc_focus
%attr(755,root,root) %{_bindir}/indi_lakeside_focus
%attr(755,root,root) %{_bindir}/indi_lx200_10micron
%attr(755,root,root) %{_bindir}/indi_lx200_16
%attr(755,root,root) %{_bindir}/indi_lx200_OpenAstroTech
%attr(755,root,root) %{_bindir}/indi_lx200_pegasus_nyx101
%attr(755,root,root) %{_bindir}/indi_lx200am5
%attr(755,root,root) %{_bindir}/indi_lx200ap_v2
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
%attr(755,root,root) %{_bindir}/indi_myDewControllerPro
%attr(755,root,root) %{_bindir}/indi_mydcp4esp32
%attr(755,root,root) %{_bindir}/indi_myfocuserpro2_focus
%attr(755,root,root) %{_bindir}/indi_nexdome_beaver
%attr(755,root,root) %{_bindir}/indi_nfocus
%attr(755,root,root) %{_bindir}/indi_nframe_rotator
%attr(755,root,root) %{_bindir}/indi_nightcrawler_focus
%attr(755,root,root) %{_bindir}/indi_nstep_focus
%attr(755,root,root) %{_bindir}/indi_onfocus_focus
%attr(755,root,root) %{_bindir}/indi_openweathermap_weather
%attr(755,root,root) %{_bindir}/indi_optec_wheel
%attr(755,root,root) %{_bindir}/indi_paramount_telescope
%attr(755,root,root) %{_bindir}/indi_pegasus_flatmaster
%attr(755,root,root) %{_bindir}/indi_pegasus_focuscube
%attr(755,root,root) %{_bindir}/indi_pegasus_focuscube3
%attr(755,root,root) %{_bindir}/indi_pegasus_ppb
%attr(755,root,root) %{_bindir}/indi_pegasus_ppba
%attr(755,root,root) %{_bindir}/indi_pegasus_prodigyMF
%attr(755,root,root) %{_bindir}/indi_pegasus_scopsoag
%attr(755,root,root) %{_bindir}/indi_pegasus_spb
%attr(755,root,root) %{_bindir}/indi_pegasus_uch
%attr(755,root,root) %{_bindir}/indi_pegasus_upb
%attr(755,root,root) %{_bindir}/indi_pegasusindigo_wheel
%attr(755,root,root) %{_bindir}/indi_perfectstar_focus
%attr(755,root,root) %{_bindir}/indi_planewave_deltat
%attr(755,root,root) %{_bindir}/indi_planewave_telescope
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
%attr(755,root,root) %{_bindir}/indi_smartfocus_focus
%attr(755,root,root) %{_bindir}/indi_snapcap
%attr(755,root,root) %{_bindir}/indi_spectracyber
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
%attr(755,root,root) %{_bindir}/indi_terrans_powerboxgo_v2
%attr(755,root,root) %{_bindir}/indi_terrans_powerboxpro_v2
%attr(755,root,root) %{_bindir}/indi_trutech_wheel
%attr(755,root,root) %{_bindir}/indi_universalror_dome
%attr(755,root,root) %{_bindir}/indi_uranus_weather
%attr(755,root,root) %{_bindir}/indi_usbdewpoint
%attr(755,root,root) %{_bindir}/indi_usbfocusv3_focus
%attr(755,root,root) %{_bindir}/indi_v4l2_ccd
%attr(755,root,root) %{_bindir}/indi_vantage_weather
%attr(755,root,root) %{_bindir}/indi_wanderer_cover
%attr(755,root,root) %{_bindir}/indi_wanderer_lite_rotator
%attr(755,root,root) %{_bindir}/indi_wanderer_rotator_lite_v2
%attr(755,root,root) %{_bindir}/indi_wanderer_rotator_mini
%attr(755,root,root) %{_bindir}/indi_wandererbox_plus_v3
%attr(755,root,root) %{_bindir}/indi_wandererbox_pro_v3
%attr(755,root,root) %{_bindir}/indi_wanderercover_v4_ec
%attr(755,root,root) %{_bindir}/indi_watchdog
%attr(755,root,root) %{_bindir}/indi_watcher_weather
%attr(755,root,root) %{_bindir}/indi_wavesharemodbus_relay
%attr(755,root,root) %{_bindir}/indi_weather_safety_proxy
%attr(755,root,root) %{_bindir}/indi_xagyl_wheel
%attr(755,root,root) %{_bindir}/indiserver
%attr(755,root,root) %{_bindir}/shelyak_usis
%attr(755,root,root) %{_libdir}/libindiAlignmentDriver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindiAlignmentDriver.so.2
%attr(755,root,root) %{_libdir}/libindiclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindiclient.so.2
%attr(755,root,root) %{_libdir}/libindidriver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindidriver.so.2
%attr(755,root,root) %{_libdir}/libindilx200.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindilx200.so.2
%dir %{_libdir}/indi
%dir %{_libdir}/indi/MathPlugins
%attr(755,root,root) %{_libdir}/indi/MathPlugins/libindi_Nearest_MathPlugin.so
%attr(755,root,root) %{_libdir}/indi/MathPlugins/libindi_SVD_MathPlugin.so
%dir %{_datadir}/indi
%{_datadir}/indi/drivers.xml
%{_datadir}/indi/indi_tcfs_sk.xml
%{_datadir}/indi/shelyak_boards.json
/lib/udev/rules.d/80-dbk21-camera.rules
/lib/udev/rules.d/99-indi_auxiliary.rules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libindiAlignmentDriver.so
%attr(755,root,root) %{_libdir}/libindiclient.so
%attr(755,root,root) %{_libdir}/libindidriver.so
%attr(755,root,root) %{_libdir}/libindilx200.so
%{_libdir}/libindiAlignmentClient.a
%{_includedir}/libindi
%{?with_qt5:%exclude %{_includedir}/libindi/baseclientqt.h}
%{_pkgconfigdir}/libindi.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libindiclient.a
%{_libdir}/libindidriver.a

%if %{with qt5}
%files qt5
%attr(755,root,root) %{_libdir}/libindiclientqt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libindiclientqt.so.2

%files qt5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libindiclientqt.so
%{_includedir}/libindi/baseclientqt.h

%files qt5-static
%defattr(644,root,root,755)
%{_libdir}/libindiclientqt.a
%endif

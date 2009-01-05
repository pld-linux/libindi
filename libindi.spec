Summary:	Instrument Neutral Distributed Interface
Name:		libindi
Version:	0.6
Release:	1
License:	LGPL
Group:		Libraries
URL:		http://indi.sourceforge.net/
Source0:	http://dl.sourceforge.net/indi/%{name}0_%{version}.tar.gz
# Source0-md5:	49218ad15a40dfa8a2366a2694477595
BuildRequires:	cfitsio-devel
BuildRequires:	cmake
BuildRequires:	libnova-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-compat-devel
BuildRequires:	zlib-devel
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
%setup -q -n %{name}0-%{version}

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	../
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
%doc AUTHORS COPYING.LIB ChangeLog NEWS README* TODO
%attr(755,root,root) %{_bindir}/indi_celestron_gps
%attr(755,root,root) %{_bindir}/indi_eval
%attr(755,root,root) %{_bindir}/indi_getprop
%attr(755,root,root) %{_bindir}/indi_intelliscope
%attr(755,root,root) %{_bindir}/indi_lx200basic
%attr(755,root,root) %{_bindir}/indi_lx200generic
%attr(755,root,root) %{_bindir}/indi_meade_lpi
%attr(755,root,root) %{_bindir}/indi_orion_atlas
%attr(755,root,root) %{_bindir}/indi_robofocus
%attr(755,root,root) %{_bindir}/indi_sbig_stv
%attr(755,root,root) %{_bindir}/indi_setprop
%attr(755,root,root) %{_bindir}/indi_skycommander
%attr(755,root,root) %{_bindir}/indi_temma
%attr(755,root,root) %{_bindir}/indi_trutech_wheel
%attr(755,root,root) %{_bindir}/indi_v4l_generic
%attr(755,root,root) %{_bindir}/indi_v4l_philips
%attr(755,root,root) %{_bindir}/indiserver
%attr(755,root,root) %ghost %{_libdir}/libindi.so.0
%attr(755,root,root) %{_libdir}/libindi.so.*.*
%{_datadir}/indi/drivers.xml
%dir %{_datadir}/indi

%files devel
%defattr(644,root,root,755)
%{_includedir}/libindi
%{_libdir}/libindi.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libindidriver.a

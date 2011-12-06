%global tarball xf86-input-wacom
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

Summary:    Xorg X11 wacom input driver
Name:       xorg-x11-drv-wacom
Version:    0.10.5
Release:    6%{?dist}
URL:        http://www.x.org
License:    GPLv2+
Group:      User Interface/X Hardware Support
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: http://prdownloads.sourceforge.net/linuxwacom/%{tarball}-%{version}.tar.bz2

# 584588 - xorg-x11-drv-wacom man page has linuxwacom reference
Patch001: wacom-0.10.5-linuxwacom-man-page.patch
# 584589 - Intuos3 scrolling issues  (note: two patches squashed)
Patch002: wacom-0.10.5-pad-scrolling.patch
# 584597 - Serial tablets should default to TPCButton on
Patch003: wacom-0.10.5-tpcbutton-on.patch
# 597932 - wacom: Pressure is always maximum in relative mode
Patch005: wacom-0.10.5-relative-pressure.patch
# 598312 - xsetwacom is missing a man page
Patch006: wacom-0.10.5-xsetwacom-man-page.patch
# 593948  - Art Pen converts valuator information into wheel events.
Patch007: wacom-0.10.5-wheel-events.patch
# 616653 - Button → keycode configurations can cause server hangs
Patch008: wacom-0.10.5-keycodes-not-keysyms.patch
# related 616653
Patch009: wacom-0.10.5-scroll-wheel-zoom.patch

ExcludeArch: s390 s390x

BuildRequires: xorg-x11-server-sdk >= 1.7.0
BuildRequires: xorg-x11-util-macros >= 1.3.0
BuildRequires: libX11-devel libXi-devel
BuildRequires: autoconf automake libtool pkgconfig

Requires:  xorg-x11-server-Xorg >= 1.7.0
Requires:  hal
Requires:  libX11 libXi

Provides:  linuxwacom = %{version}-%{release}
Obsoletes: linuxwacom <= 0.8.4.3

%description
X.Org X11 wacom input driver for Wacom tablets.

%prep
%setup -q -n %{tarball}-%{version}

%patch001 -p1
%patch002 -p1
%patch003 -p1
%patch005 -p1
%patch006 -p1
%patch007 -p1
%patch008 -p1
%patch009 -p1

%build
autoreconf -v --install || exit 1
%configure --disable-static
make %{_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

install -d $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty
install -m 0644 ${RPM_BUILD_ROOT}%{_datadir}/hal/fdi/policy/20thirdparty/wacom.fdi $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty/10-wacom.fdi
rm ${RPM_BUILD_ROOT}%{_datadir}/hal/fdi/policy/20thirdparty/wacom.fdi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README GPL
%{driverdir}/wacom_drv.so
%{_mandir}/man4/wacom.4*
%{_mandir}/man1/xsetwacom.1*
%{_datadir}/hal/fdi/policy/20thirdparty/10-wacom.fdi
%{_bindir}/xsetwacom


%package devel
Summary:    Xorg X11 wacom input driver development package
Group:      Development/Libraries

Requires: xorg-x11-server-devel >= 1.7.0
Requires: pkgconfig

%description devel
X.Org X11 wacom input driver development files.

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/xorg-wacom.pc
%{_includedir}/xorg/Xwacom.h
%{_includedir}/xorg/wacom-properties.h

%changelog
* Wed Jul 28 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-6
- wacom-0.10.5-keycodes-not-keysyms.patch: load keycodes into the driver,
  not keysyms. Avoids server hangs when XkbGetCoreMap() allocs in signal
  handler (#616653)
- wacom-0.10.5-scroll-wheel-zoom.patch: zoom with wheel, not ctrl+/- since
  the latter is now layout-dependent.

* Mon Jun 21 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-5
- wacom-0.10.5-wheel-events.patch: don't convert the wheel events to scroll
  events for anything but the pad (#593948)

* Thu Jun 10 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-4
- Remove wacom-0.10.5-axis-mode.patch: this is an X server bug (#594523)
- wacom-0.10.5-relative-pressure.patch: subtract old pressure from new
  pressue values to get a relative value (#597932)
- wacom-0.10.05-xsetwacom-man-page.patch: add xsetwacom man page (#598312)

* Wed May 26 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-3
- wacom-0.10.5-axis-mode.patch: don't merge OutOfProximity flags to axis
  mode (#594523)

* Thu Apr 22 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-2
- wacom-0.10.5-linuwacom-man-page.patch: drop reference to linuxwacom from
  man page (#584588)
- wacom-0.10.5-pad-scrolling.patch: force relative mode for pad (#584589)
- wacom-0.10.5-tpcbutton-on.patch: enable TPCButton for ISDV4 devices
  (#584597)

* Fri Mar 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-1
- wacom 0.10.5 (#575014)
- wacom-0.10.4-license-fix.patch: Drop, upstream.

* Fri Feb 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-2
- wacom-0.10.4-license-fix.patch: fix license copy/paste errors. Patch from
  upstream (#566622)

* Wed Feb 03 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-1
- wacom 0.10.4
- Update sources to point to sourceforge.
- Install the upstream fdi file instead of our custom one.
- Update Requires and BuildRequires for xsetwacom.

* Mon Nov 23 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.1-2
- 10-linuxwacom.fdi: squash extra entry for bluetooth tablet into general
  Wacom match. 
- 10-linuxwacom.fdi: remove info.parent condition for N-Trig (#538036)

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.1-1
- wacom 0.10.1
- Remove unnecessary 'find' directive, changed upstream.
- Add GPL document
- Install 10-wacom.fdi file.
- Provides: linuxwacom

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-4
- BuildRequires xorg-x11-util-macros 1.3.0

* Thu Nov 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-3
- Use smp_mflags when building.

* Wed Nov 18 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-2
- Obsolete linuxwacom, don't Conflict with it.
- Remove trailing dot from summary (rpmlint warning).
- Remove spurious executable bits from source files (rpmlint warning).
- Add AUTHORS, ChangeLog, README to doc

* Mon Oct 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-1
- Initial import


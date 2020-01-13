%global codename madrid
Name: el-logos
Summary: EL related icons and pictures
Version: 70.0.5
Release: 2.0%{?dist}
Group: System Environment/Base
URL: http://www.euro-linux.com
Source0: el-logos-%{version}.tar.bz2
License: GPL+, CC-BY-SA

BuildArch: noarch

# SL added for optimizing images
BuildRequires:	findutils
# These are in EPEL, but are super useful for keeping things clean
BuildRequires:	jpegoptim
BuildRequires:	optipng

Obsoletes: gnome-logos
Obsoletes: fedora-logos <= 16.0.2-2

Provides: gnome-logos = %{version}-%{release}
Provides: system-logos = %{version}-%{release}
Provides: redhat-logos = %{version}-%{release}
Provides: linux-logos = %{version}-%{release}
Provides: scientific-linux-logos = %{version}-%{release}
Provides: sl-logos = %{version}-%{release}
Provides: centos-logos = %{version}-%{release}
# We carry the GSettings schema override, tell that to gnome-desktop3
Provides: system-backgrounds-gnome

Conflicts: kdebase <= 3.1.5
Conflicts: anaconda-images <= 10
Conflicts: redhat-artwork <= 5.0.5

Requires(post): coreutils
BuildRequires: hardlink
# For _kde4_* macros:
BuildRequires: kde-filesystem

# SL added for our GDM theme
Requires(post): policycoreutils

%description
EuroLinux artwork and branding

See the included COPYING file for information on copying and
redistribution.

%prep
%setup -q

%build
echo 'Optimizing images, you probably should have already done this....'
find . -type f -name \*.png -exec optipng -strip all {} \;
find . -type f -name \*.jpg -exec jpegoptim --all-normal -s  {} \;
find . -type f -name \*.jpeg -exec jpegoptim --all-normal -s  {} \;

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/backgrounds/
for type in xml png jpg jpeg; do
    for i in $(find backgrounds -type f -name \*.${type}); do
      install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/backgrounds/
    done
done

# set Fixation to our default background
cp $RPM_BUILD_ROOT%{_datadir}/backgrounds/Fixation.xml $RPM_BUILD_ROOT%{_datadir}/backgrounds/default.xml

mkdir -p $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas
install -p -m 644 backgrounds/10_org.gnome.desktop.background.default.gschema.override $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas
install -p -m 644 backgrounds/10_org.gnome.desktop.screensaver.default.gschema.override $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties/
install -p -m 644 backgrounds/desktop-backgrounds-default.xml $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/firstboot/themes/fedora-%{codename}/
for i in firstboot/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/firstboot/themes/fedora-%{codename}/
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
for i in pixmaps/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/pixmaps
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
for i in plymouth/charge/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
done

for size in 16x16 22x22 24x24 32x32 36x36 48x48 96x96 256x256 ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps
  for i in icons/hicolor/$size/apps/* ; do
    install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
    cp icons/hicolor/$size/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps/icon-panel-menu.png
    cp icons/hicolor/$size/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps/gnome-main-menu.png
    cp icons/hicolor/$size/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps/kmenu.png
    cp icons/hicolor/$size/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps/start-here.png
  done
done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
pushd $RPM_BUILD_ROOT%{_sysconfdir}
ln -s %{_datadir}/icons/hicolor/16x16/apps/fedora-logo-icon.png favicon.png
popd

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/xfce4_xicon1.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/fedora-logo-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/start-here.svg

(cd anaconda; make DESTDIR=$RPM_BUILD_ROOT install)

for i in 16 22 24 32 36 48 96 256 ; do
  install -p -m 644 -D $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/${i}x${i}/places/start-here-kde-fedora.png 
done

# ksplash theme
mkdir -p $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/
cp -rp kde-splash/RHEL7/ $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/
pushd $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/RHEL7/2560x1600/
ln -s %{_datadir}/pixmaps/system-logo-white.png logo.png
popd

# kdm theme
mkdir -p $RPM_BUILD_ROOT/%{_kde4_appsdir}/kdm/themes/
cp -rp kde-kdm/RHEL7/ $RPM_BUILD_ROOT/%{_kde4_appsdir}/kdm/themes/
pushd $RPM_BUILD_ROOT/%{_kde4_appsdir}/kdm/themes/RHEL7/
ln -s %{_datadir}/pixmaps/system-logo-white.png system-logo-white.png
popd

# kde wallpaper theme
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/wallpapers/
cp -rp kde-plasma/RHEL7/ $RPM_BUILD_ROOT/%{_datadir}/wallpapers
pushd $RPM_BUILD_ROOT/%{_datadir}/wallpapers/RHEL7/contents/images
ln -s %{_datadir}/backgrounds/Fixation-2k.jpg 2560x1600.jpg
popd
pushd $RPM_BUILD_ROOT/%{_datadir}/wallpapers/
ln -s %{_datadir}/backgrounds .
popd

# kde desktop theme
mkdir -p $RPM_BUILD_ROOT/%{_kde4_appsdir}/desktoptheme/
cp -rp kde-desktoptheme/* $RPM_BUILD_ROOT/%{_kde4_appsdir}/desktoptheme/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a fedora/*.svg $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a fedora/*.png $RPM_BUILD_ROOT%{_datadir}/%{name}

# save some dup'd icons
/usr/sbin/hardlink -v %{buildroot}/

%post
touch --no-create %{_datadir}/icons/hicolor || :
touch --no-create %{_datadir}/icons/Bluecurve || :
touch --no-create %{_kde4_iconsdir}/oxygen ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor || :
  touch --no-create %{_datadir}/icons/Bluecurve || :
  touch --no-create %{_kde4_iconsdir}/oxygen ||:
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/Bluecurve &>/dev/null || :
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &>/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/Bluecurve &>/dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

# BZ 1096986
# load our SL gdm theme
%triggerin -- gnome-shell
if [[ -f %{_docdir}/%{name}-%{version}/sl-gdm-theme/noise-texture.png ]]; then
    cp -f %{_docdir}/%{name}-%{version}/sl-gdm-theme/noise-texture.png %{_datadir}/gnome-shell/theme/ >/dev/null 2>&1
    restorecon %{_datadir}/gnome-shell/theme/noise-texture.png >/dev/null 2>&1
fi

%files
%doc COPYING sl-gdm-theme
%config(noreplace) %{_sysconfdir}/favicon.png
%{_datadir}/backgrounds/*
%{_datadir}/glib-2.0/schemas/*.override
%{_datadir}/gnome-background-properties/*
%{_datadir}/firstboot/themes/fedora-%{codename}/
%{_datadir}/plymouth/themes/charge/
%{_kde4_iconsdir}/oxygen/
%{_kde4_appsdir}/ksplash/Themes/RHEL7/
%{_kde4_appsdir}/kdm/themes/RHEL7/
%{_kde4_datadir}/wallpapers/*
%{_kde4_appsdir}/desktoptheme/RHEL7/

%{_datadir}/pixmaps/*
%{_datadir}/anaconda/boot/splash.lss
%{_datadir}/anaconda/boot/syslinux-splash.png
%{_datadir}/anaconda/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/Bluecurve/*/apps/*
%{_datadir}/%{name}/

# we multi-own these directories, so as not to require the packages that
# provide them, thereby dragging in excess dependencies.
%dir %{_datadir}/icons/Bluecurve/
%dir %{_datadir}/icons/Bluecurve/16x16/
%dir %{_datadir}/icons/Bluecurve/16x16/apps/
%dir %{_datadir}/icons/Bluecurve/22x22/
%dir %{_datadir}/icons/Bluecurve/22x22/apps/
%dir %{_datadir}/icons/Bluecurve/24x24/
%dir %{_datadir}/icons/Bluecurve/24x24/apps/
%dir %{_datadir}/icons/Bluecurve/32x32/
%dir %{_datadir}/icons/Bluecurve/32x32/apps/
%dir %{_datadir}/icons/Bluecurve/36x36/
%dir %{_datadir}/icons/Bluecurve/36x36/apps/
%dir %{_datadir}/icons/Bluecurve/48x48/
%dir %{_datadir}/icons/Bluecurve/48x48/apps/
%dir %{_datadir}/icons/Bluecurve/96x96/
%dir %{_datadir}/icons/Bluecurve/96x96/apps/
%dir %{_datadir}/icons/Bluecurve/256x256/
%dir %{_datadir}/icons/Bluecurve/256x256/apps/
%dir %{_datadir}/icons/hicolor/
%dir %{_datadir}/icons/hicolor/16x16/
%dir %{_datadir}/icons/hicolor/16x16/apps/
%dir %{_datadir}/icons/hicolor/22x22/
%dir %{_datadir}/icons/hicolor/22x22/apps/
%dir %{_datadir}/icons/hicolor/24x24/
%dir %{_datadir}/icons/hicolor/24x24/apps/
%dir %{_datadir}/icons/hicolor/32x32/
%dir %{_datadir}/icons/hicolor/32x32/apps/
%dir %{_datadir}/icons/hicolor/36x36/
%dir %{_datadir}/icons/hicolor/36x36/apps/
%dir %{_datadir}/icons/hicolor/48x48/
%dir %{_datadir}/icons/hicolor/48x48/apps/
%dir %{_datadir}/icons/hicolor/96x96/
%dir %{_datadir}/icons/hicolor/96x96/apps/
%dir %{_datadir}/icons/hicolor/256x256/
%dir %{_datadir}/icons/hicolor/256x256/apps/
%dir %{_datadir}/icons/hicolor/scalable/
%dir %{_datadir}/icons/hicolor/scalable/apps/
%dir %{_datadir}/anaconda
%dir %{_datadir}/anaconda/pixmaps
%dir %{_datadir}/anaconda/boot/
%dir %{_datadir}/firstboot/
%dir %{_datadir}/firstboot/themes/
%dir %{_datadir}/plymouth/
%dir %{_datadir}/plymouth/themes/
%dir %{_kde4_sharedir}/kde4/
%dir %{_kde4_appsdir}
%dir %{_kde4_appsdir}/ksplash
%dir %{_kde4_appsdir}/ksplash/Themes/

%changelog
* Mon Dec 23 2019 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> - 70.0.5-2.0
- Version up for build system.

* Thu Nov 29 2018 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> - 70.0.5-1.0
- Fix screen saver && pull from upstream.

* Mon Aug  8 2016 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> - 70.0.5-0.0
- Release up, fixing EuroLinux 7.0 wrong package release

* Tue Apr 19 2016 Aleksander Baranowski <aleksander.baranowski@euro-linux.com> - 70.0.3-0.11
- Fix icons for 32x32

* Fri Aug 14 2015 Alex Baranowski <aleksander.baranowski@euro-linux.com> - 70.0.3-0.10
- EuroLinux 7 branding v.2

* Thu Aug 13 2015 Alex Baranowski <aleksander.baranowski@euro-linux.com> - 70.0.3-0.8
- EuroLinux 7 branding v.1

* Wed Feb 25 2015 Pat Riehecky <riehecky@fnal.gov> - 70.0.3-0.7
- Fine, no plymouth watermark as I can't get it centered.....

* Wed Aug 13 2014 Pat Riehecky <riehecky@fnal.gov> - 70.0.3-0.6
- Fixed KDE artwork links

* Fri Jun 13 2014 Pat Riehecky <riehecky@fnal.gov> - 70.0.3-0.5
- Revised fedora-gdm-logo picture (again)
- Revised plymoth splash screen
- now running image optimizations before packaging

* Tue May 13 2014 Pat Riehecky <riehecky@fnal.gov> - 70.0.3-0.4
- Revised fedora-gdm-logo picture

* Tue May 13 2014 Pat Riehecky <riehecky@fnal.gov> - 70.0.3-0.3
- Revised GDM theme

* Tue May 13 2014 Pat Riehecky <riehecky@fnal.gov> - 70.0.3-0.2
- Added GDM theme

* Mon May 12 2014 Pat Riehecky <riehecky@fnal.gov> - 70.0.3-0.1
- Added Fixation theme

* Tue May 06 2014 Pat Riehecky <riehecky@fnal.gov> - 70.0.3-0
- Initial build for SL7


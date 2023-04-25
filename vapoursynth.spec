%define major 0
%define api 61
%define libname %mklibname %{name} %{major}
%define libscript %mklibname vapoursynth-script %{major}
%define devname %mklibname %{name} -d

%define _disable_ld_no_undefined 1
%define _disable_lto 1

Summary:	A video processing framework with the future in mind
Name:		vapoursynth
Version:	R62
Release:	1
License:	LGPLv2
Group:		Video
Url:		http://www.vapoursynth.com/
Source0:	https://github.com/vapoursynth/vapoursynth/archive/R%{version}/%{name}-%{version}.tar.gz
Patch1:   vapoursynth-version.patch

BuildRequires:  libtool
BuildRequires:  nasm
BuildRequires:	yasm
BuildRequires:  pkgconfig(python)
BuildRequires:  pkgconfig(tesseract)
BuildRequires:  pkgconfig(zimg)
BuildRequires:  python
BuildRequires:  python3dist(setuptools)
BuildRequires:	python3dist(cython)
BuildRequires:	python3dist(sphinx)
BuildRequires:	shared-mime-info
BuildRequires:	ffmpeg-devel
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)

# Optional
BuildRequires:  pkgconfig(Magick++) >= 7.0

Obsoletes:	%{name}-plugins =< R56 
Requires:	ffmpeg
Requires:	tesseract

%description
VapourSynth is an application for video manipulation. Or a plugin. Or a
library. It’s hard to tell because it has a core library written in C++
and a Python module to allow video scripts to be created. It came to be
when I started thinking about alternative designs for Avisynth and most
of it was written over a 3 month period.

The software has been heavily inspired by Avisynth and aims to be a 21st
century rewrite, taking advantage of the advancements computers have made
since the late 90s.

The main features compared to Avisynth are:

* Multithreaded
  - Frame level multithreading that scales well
* Generalized Colorspaces
  - New colorspaces can be specified at runtime
* Per Frame Properties
  - Additional metadata can be attached to frames
* Python Based
  - The scripting part is implemented as a Python module so you don’t have
    to learn a special language
* Support for video with format changes
  - Some video just can’t stick to one format or frame size.
* Compatible with a large number of already existing Avisynth plugins

%files
%doc ChangeLog
%{_bindir}/*

#----------------------------------------------------------------------------

#package plugins
#Summary:	Plugins for %{name}
#Group:		Video
#Requires:	%{name} = %{EVRD}
#
#description plugins
#Plugins package for %{name}
#
#files plugins
#doc ChangeLog
#{_libdir}/vapoursynth/libassvapour.so
#{_libdir}/vapoursynth/libeedi3.so
#{_libdir}/vapoursynth/libmorpho.so
#_libdir}/vapoursynth/libocr.so
#{_libdir}/vapoursynth/libremovegrain.so
#{_libdir}/vapoursynth/libvinverse.so
#{_libdir}/vapoursynth/libvivtc.so
#{_libdir}/vapoursynth/libsubtext.so
#_libdir}/vapoursynth/libmiscfilters.so
#_libdir}/vapoursynth/libimwri.so

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Shared library for %{name}.

%files -n %{libname}
%doc ChangeLog
%{_libdir}/libvapoursynth-%{api}.so

#----------------------------------------------------------------------------

%package -n %{libscript}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}vapoursynth0 < R26-2

%description -n %{libscript}
Shared library for %{name}.

%files -n %{libscript}
%doc ChangeLog
%{_libdir}/libvapoursynth-script.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Requires:	%{libscript} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}vapoursynth-static-devel < R26-2

%description -n %{devname}
Development files and headers for %{name}.

%files -n %{devname}
%doc ChangeLog
%{_includedir}/%{name}
%{_libdir}/libvapoursynth.so
%{_libdir}/libvapoursynth-script.so
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Python bindings for %{name}
Group:		Development/Python
Requires:	%{libname} = %{EVRD}
BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(setuptools)

%description -n python-%{name}
Python bindings for %{name}.


%files -n python-%{name}
%doc ChangeLog
%{py3_platsitedir}/vapoursynth.so
%{python_sitearch}/VapourSynth-%{api}-py*.*.egg-info


#----------------------------------------------------------------------------

%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains documentation of %{name}.

%files doc
%doc doc/

#----------------------------------------------------------------------------

%prep
%autosetup -p1 %{name}-%{version}

%build
autoreconf -vif
%configure \
    --disable-static \
    --enable-x86-asm \
    --enable-core \
    --enable-vsscript \
    --enable-vspipe \
    --enable-python-module \
    --enable-eedi3 \
    --enable-ImageMagick \
    --enable-miscfilters \
    --enable-morpho \
    --enable-ocr \
    --enable-removegrain \
    --enable-ffmpeg \
    --enable-vinverse \
    --enable-vivtc
 
%make_build
 
%install
%py_install
%make_install

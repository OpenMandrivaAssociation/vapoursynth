%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define statname        %mklibname %{name} -s -d


Summary:	A video processing framework with the future in mind
Name:		vapoursynth
Version:	R26
Release:	1
License:	OFL and LGPLv2.1
Group:		Video
Url:		http://www.vapoursynth.com/
Source0:	https://github.com/vapoursynth/vapoursynth/archive/%{version}.tar.gz
Source1:	vapoursynth.xml
BuildRequires:	python3egg(cython)
BuildRequires:	python3egg(sphinx)
BuildRequires:	yasm
BuildRequires:	ffmpeg-devel
BuildRequires:	shared-mime-info
BuildRequires:	pkgconfig(tesseract)

Requires:	%{libname} = %{EVRD}
Requires:	%{name}-plugins = %{EVRD}
Requires:	ffmpeg
Requires:	tesseract

%description
VapourSynth is an application for video manipulation. 
Or a plugin. Or a library. It’s hard to tell because 
it has a core library written in C++ and a Python 
module to allow video scripts to be created. 
It came to be when I started thinking about 
alternative designs for Avisynth and most of 
it was written over a 3 month period.

The software has been heavily inspired by 
Avisynth and aims to be a 21st century rewrite, 
taking advantage of the advancements 
computers have made since the late 90s. 
The main features compared to Avisynth are:

Multithreaded 
  - Frame level multithreading that scales well
Generalized Colorspaces 
  - New colorspaces can be specified at runtime
Per Frame Properties 
  - Additional metadata can be attached to frames
Python Based 
  - The scripting part is implemented as a 
  Python module so you don’t have 
  to learn a special language
Support for video with format changes 
  - Some video just can’t stick to one format or frame size. 
  VapourSynth can handle any kind of change
Compatible with a large number of already 
existing Avisynth plugins


%files
%doc ofl.txt COPYING.LGPLv2.1 ChangeLog
%{_bindir}/*
%{_datadir}/mime/packages/*

#--------------------------------------------

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description -n %{libname}
Main library for %{name}.

%files -n %{libname}
%doc ofl.txt COPYING.LGPLv2.1 ChangeLog
%{_libdir}/*.so.%{major}*


#--------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Requires:	%{name}-plugins = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}

%description -n %{develname}
Development files and headers for %{name}.

%files -n %{develname}
%doc ofl.txt COPYING.LGPLv2.1 ChangeLog
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
#--------------------------------------------

%package -n	%{statname}

Group:		Development/C
Summary:	Static library for the %{name} codec library
Requires:	%{develname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n	%{statname}
Install this package if you want to compile static apps 
with %{name} support.

%files -n %{statname}
%doc ofl.txt COPYING.LGPLv2.1 ChangeLog
%{_libdir}/*.a
#--------------------------------------------
%package -n	%{name}-plugins

Group:		Development/C
Summary:	Plugins for %{name}
Requires:	%{name} = %{EVRD}

%description -n	%{name}-plugins
Plugins package for %{name}

%files -n %{name}-plugins
%doc ofl.txt COPYING.LGPLv2.1 ChangeLog
%{_libdir}/vapoursynth/libassvapour.so
%{_libdir}/vapoursynth/libeedi3.so
%{_libdir}/vapoursynth/libmorpho.so
%{_libdir}/vapoursynth/libocr.so
%{_libdir}/vapoursynth/libremovegrain.so
%{_libdir}/vapoursynth/libvinverse.so
%{_libdir}/vapoursynth/libvivtc.so

%package -n python3-%{name}
Summary:	Python bindings for %{name}
Group:		Development/Python
Requires:	%{libname} = %{EVRD}
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3egg(setuptools)

%description -n python3-%{name}
Python bindings for %{name}.


%files -n python3-%{name}
%doc ofl.txt COPYING.LGPLv2.1 ChangeLog
%{py3_platsitedir}/vapoursynth.so
#--------------------------------------------

%package doc
Summary:	Documentation for %{name} 
Group:		Development/Other

%description doc
This package contains documentation of %{name}.

%files doc
%doc doc/
#--------------------------------------------

%prep
%setup -q


%build
./autogen.sh
%configure2_5x
%make

%install
%makeinstall_std
install -dm 755 %{buildroot}%{_datadir}/mime/packages
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/mime/packages

pushd doc
rm -f conf.py make.bat Makefile 
popd


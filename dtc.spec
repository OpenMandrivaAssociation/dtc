%define api 1
%define major 4
%define libname %mklibname fdt %{api} %{major}
%define devname %mklibname -d fdt %{api}
%define devnamestatic %mklibname -d fdt_static %{api}

Name:		dtc
Version:	1.6.1
Release:	1
Summary:	Device Tree Compiler
Group:		Development/Other
License:	GPLv2+
URL:		http://devicetree.org/Device_Tree_Compiler
Source0:	https://www.kernel.org/pub/software/utils/dtc/%{name}-%{version}.tar.xz
Patch0:		dtc-1.6.1-our-clang-has-gnuc4.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	swig
BuildRequires:	pkgconfig(python3)

%description
The Device Tree Compiler generates flattened Open Firmware style device trees
for use with PowerPC machines that lack an Open Firmware implementation and
ARM/AArch64 devices that don't implement UEFI.

%package -n %{libname}
Summary:	Device tree library
Group:		System/Libraries

%description -n %{libname}
libfdt is a library to process Open Firmware style device trees on various
architectures.

%package -n %{devname}
Summary:	Development headers for device tree library
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	fdt-devel = %{version}-%{release}

%description -n %{devname}
This package provides development files for libfdt.

%package -n %{devnamestatic}
Summary:	Development headers for device tree library
Group:		System/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	fdt-static-devel = %{version}-%{release}

%description -n	%{devnamestatic}
This package provides development files for libfdt.

%package -n python-%{name}
Summary:	Python 2 bindings for %{name}
Provides:	python3-libfdt = %{EVRD}
Requires:	%{name} = %{EVRD}

%description -n python-%{name}
This package provides python3 bindings for %{name}.

%prep
%autosetup -p1
sed -i 's/python2/python3/' pylibfdt/setup.py

%build
%set_build_flags

sed -i \
	-e '/^CFLAGS =/s:=:+= %{optflags}:' \
	-e '/^CPPFLAGS =/s:=:+=:' \
	-e '/^WARNINGS =/s:=:+=:' \
	-e "/^PREFIX =/s:=.*:= %{_prefix}:" \
	-e "/^LIBDIR =/s:=.*:= \%{_libdir}:" \
	Makefile

# no-macro-redefined is a workaround for flex bug
# https://github.com/westes/flex/issues/155
%make_build CC=%{__cc} LDFLAGS="%{optflags}" WARNINGS+=-Wno-macro-redefined

%install
%make_install DESTDIR=$RPM_BUILD_ROOT PREFIX=$RPM_BUILD_ROOT/usr \
             LIBDIR=%{_libdir} BINDIR=%{_bindir} INCLUDEDIR=%{_includedir} V=1

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libfdt-%{version}.so
%{_libdir}/libfdt.so.*

%files -n %{devname}
%doc GPL
%{_libdir}/libfdt.so
%{_includedir}/*

%files -n %{devnamestatic}
%{_libdir}/libfdt.a

%files -n python-%{name}
%{python3_sitearch}/*

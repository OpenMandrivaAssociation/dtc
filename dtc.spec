%define api 1
%define major 4
%define libname %mklibname fdt %{api} %{major}
%define devname %mklibname -d fdt %{api}

Name:		dtc
Version:	1.4.5
Release:	1
Summary:	Device Tree Compiler
Group:		Development/Other
License:	GPLv2+
URL:		http://devicetree.org/Device_Tree_Compiler
Source0:	https://www.kernel.org/pub/software/utils/dtc/%{name}-%{version}.tar.xz
Patch0:		use-tx-as-the-type-specifier-instead-of-zx.patch
Patch1:		checks-Use-proper-format-modifier-for-size_t.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	swig
BuildRequires:	pkgconfig(python2)

%description
The Device Tree Compiler generates flattened Open Firmware style device trees
for use with PowerPC machines that lack an Open Firmware implementation and
ARM/AArch64 devices that don't implement UEFI.

%package -n	%{libname}
Summary:	Device tree library
Group:		System/Libraries

%description -n %{libname}
libfdt is a library to process Open Firmware style device trees on various
architectures.

%package -n	%{devname}
Summary:	Development headers for device tree library
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	fdt-devel = %{version}-%{release}

%description -n	%{devname}
This package provides development files for libfdt

%package -n python2-%{name}
Summary:	Python 2 bindings for %{name}
Requires:	%{name} = %{EVRD}

%description -n python2-%{name}
This package provides python2 bindings for %{name}.

%prep
%setup -q
%apply_patches

%build
%setup_compile_flags

sed -i \
	-e '/^CFLAGS =/s:=:+= %{optflags}:' \
	-e '/^CPPFLAGS =/s:=:+=:' \
	-e '/^WARNINGS =/s:=:+=:' \
	-e "/^PREFIX =/s:=.*:= %{_prefix}:" \
	-e "/^LIBDIR =/s:=.*:= \%{_libdir}:" \
	Makefile

# no-macro-redefined is a workaround for flex bug
# https://github.com/westes/flex/issues/155
%make CC=%{__cc} LDFLAGS="%{optflags}" WARNINGS+=-Wno-macro-redefined

%install
%makeinstall_std SETUP_PREFIX=%{buildroot}%{_prefix} PREFIX=%{_prefix} LIBDIR=%{_libdir}
find %{buildroot} -type f -name "*.a" -delete

# we don't want or need ftdump and it conflicts with freetype-demos, so drop
# it (rhbz 797805)
rm -f %{buildroot}/%{_bindir}/ftdump

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libfdt-%{version}.so
%{_libdir}/libfdt.so.*

%files -n %{devname}
%doc GPL
%{_libdir}/libfdt.so
%{_includedir}/*

%files -n python2-%{name}
%{python_sitearch}/*

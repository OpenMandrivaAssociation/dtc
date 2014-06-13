%define api 1
%define major   4
%define libname %mklibname fdt %{api} %{major}
%define devname %mklibname -d fdt %{api}

Name:		dtc
Version:	1.4.0
Release:	6
Summary:	Device Tree Compiler
Group:		Development/Other
License:	GPLv2+
URL:		http://git.jdl.com/gitweb/?p=dtc.git;a=summary
Source0:	http://www.jdl.com/software/dtc-v%{version}.tgz
Patch0:		use-tx-as-the-type-specifier-instead-of-zx.patch

BuildRequires:	bison
BuildRequires:	flex

%description
The Device Tree Compiler generates flattened Open Firmware style device trees
for use with PowerPC machines that lack an Open Firmware implementation

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

%prep
%setup -qn dtc-v%{version}
%apply_patches

%build
%make

%install
%makeinstall_std PREFIX=/usr LIBDIR=%{_libdir}
rm -rf %{buildroot}/%{_libdir}/*.a

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

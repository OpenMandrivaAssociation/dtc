%define major 1
%define libname %mklibname fdt %{major}
%define devname %mklibname -d fdt
%define devnamestatic %mklibname -d -s fdt

Name:		dtc
Version:	1.7.0
Release:	3
Summary:	Device Tree Compiler
Group:		Development/Other
License:	GPLv2+
URL:		https://devicetree.org/Device_Tree_Compiler
Source0:	https://www.kernel.org/pub/software/utils/dtc/%{name}-%{version}.tar.gz
Patch0:		dtc-1.6.1-our-clang-has-gnuc4.patch
Patch1:		dtc-1.7.0-meson-fix-version.patch
# (tpg) upstream patch
Patch100:	https://git.kernel.org/pub/scm/utils/dtc/dtc.git/patch/?id=71a8b8ef0adf01af4c78c739e04533a35c1dc89c.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	swig
BuildRequires:	meson
BuildRequires:	pkgconfig(yaml-0.1)
BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(setuptools-scm)

%description
The Device Tree Compiler generates flattened Open Firmware style device trees
for use with PowerPC machines that lack an Open Firmware implementation and
ARM/AArch64 devices that don't implement UEFI.

%package -n %{libname}
Summary:	Device tree library
Group:		System/Libraries
Obsoletes:	%{mklibname fdt 1 4} < 1.7.0-1

%description -n %{libname}
libfdt is a library to process Open Firmware style device trees on various
architectures.

%package -n %{devname}
Summary:	Development headers for device tree library
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	fdt-devel = %{version}-%{release}
Obsoletes:	%{mklibname -d fdt 1} < 1.7.0-1

%description -n %{devname}
This package provides development files for libfdt.

%package -n %{devnamestatic}
Summary:	Development headers for device tree library
Group:		System/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	fdt-static-devel = %{version}-%{release}
Obsoletes:	%{mklibname -d fdt_static 1} < 1.7.0-1

%description -n %{devnamestatic}
This package provides development files for libfdt.

%package -n python-%{name}
Summary:	Python 2 bindings for %{name}
Provides:	python3-libfdt = %{EVRD}
Requires:	%{name} = %{EVRD}

%description -n python-%{name}
This package provides python3 bindings for %{name}.

%prep
%autosetup -p1

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%meson -Dvalgrind=disabled

%ninja_build -C build

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%ninja_install -C build

rm -f %{buildroot}%{_bindir}/ftdump

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libfdt.so.%{major}*

%files -n %{devname}
%doc GPL
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libfdt.so
%{_includedir}/*

%files -n %{devnamestatic}
%{_libdir}/libfdt.a

%files -n python-%{name}
%{python3_sitearch}/*

# Tag v23.10.0
%global commit0 3952b468c9da89edad9dff953cdcab0a3c3bf78c
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20231030
%global upstream_name AdaptiveCpp
# Uses this version of clang
%global llvm_maj_ver 17

Summary:        An implementation of SYCL
Name:           adaptivecpp
License:        BSD-2-Clause
Version:        23.10.0
Release:        1%{?dist}

URL:            https://github.com/AdaptiveCpp/AdaptiveCpp
Source0:        %{url}/archive/%{commit0}/%{upstream_name}-%{shortcommit0}.tar.gz
Patch0:         0001-prepare-adaptivecpp-cmake-for-fedora.patch
Patch1:         0001-adaptivecpp-do-not-use-rpath-in-link.patch
Patch2:         0001-acpp-config-file-is-installed-to-system.patch
Patch3:         0001-acpp-use-lib64-dir.patch
Patch4:         0001-backend_loader-use-lib64-library.patch

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: gtest-devel

BuildRequires:  clang-devel
BuildRequires:  clang(major) = %{llvm_maj_ver}
BuildRequires:  llvm-devel(major) = %{llvm_maj_ver}
Requires:       clang(major) = %{llvm_maj_ver}
Requires:       clang-resource-filesystem

%description
AdaptiveCpp is the independent, community-driven modern platform for
C++-based heterogeneous programming models targeting CPUs and GPUs
from all major vendors. AdaptiveCpp lets applications adapt themselves
to all the hardware found in the system. This includes use cases where
a single binary needs to be able to target all supported hardware,
or utilize hardware from different vendors simultaneously.

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}

%prep
%autosetup -p1 -n %{upstream_name}-%{commit0}

%build

%cmake \
    -DCMAKE_BUILD_TYPE=DEBUG \
    -DACPP_VERSION_SUFFIX=+git.%{shortcommit0}.%{date} \
    -DSYCLCC_CONFIG_FILE_GLOBAL_INSTALLATION=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DWITH_CUDA_BACKEND=OFF \
    -DWITH_ROCM_BACKEND=ON \
    -DWITH_OPENCL_BACKEND=OFF \
    -DWITH_ACCELERATED_CPU=OFF

%cmake_build

# tests require AdaptiveCpp to be packaged first
# %check

%install
%cmake_install

find %{buildroot}%{_includedir}/%{upstream_name} -type d  > dirs.files
echo "s|%{buildroot}%{_includedir}/%{upstream_name}|%%dir %%{_includedir}/%%{upstream_name}|g" > br.sed
sed -i -f br.sed dirs.files 
cat dirs.files > main.files

# Find the headers
find %{buildroot}%{_includedir}/%{upstream_name} -type f -name "*.h"  -o -name "*.hpp" > devel.files
echo "s|%{buildroot}%{_includedir}/%{upstream_name}|%%{_includedir}/%%{upstream_name}|g" > br.sed
sed -i -f br.sed devel.files 

%ldconfig_post

%ldconfig_postun

%files -f main.files
%dir %{_libdir}/cmake/hipSYCL
%dir %{_libdir}/cmake/OpenSYCL
%dir %{_libdir}/cmake/%{upstream_name}
%dir %{_libdir}/hipSYCL
%dir %{_libdir}/hipSYCL/llvm-to-backend

%license LICENSE

%{_sysconfdir}/hipSYCL/syclcc.json

# bins
%{_bindir}/acpp
%{_bindir}/acpp-hcf-tool
%{_bindir}/acpp-info
%{_bindir}/syclcc
%{_bindir}/syclcc-clang
# misc tool
%{_libdir}/hipSYCL/llvm-to-backend/llvm-to-amdgpu-tool

# bitcodes
%{_libdir}/hipSYCL/bitcode/*.bc

# libs
%{_libdir}/libacpp-clang.so.*
%{_libdir}/libacpp-common.so.*
%{_libdir}/libacpp-rt.so.*
%{_libdir}/libllvm-to-amdgpu.so.*
%{_libdir}/libllvm-to-backend.so.*
# These are dlopened
%{_libdir}/hipSYCL/librt-backend-hip.so
%{_libdir}/hipSYCL/librt-backend-omp.so



%files devel -f devel.files
%doc README.md

# misc headers
%{_includedir}/%{upstream_name}/hipSYCL/std/hiplike/bits/basic_string.tcc
%{_includedir}/%{upstream_name}/hipSYCL/std/hiplike/complex
%{_includedir}/%{upstream_name}/hipSYCL/std/stdpar/algorithm
%{_includedir}/%{upstream_name}/hipSYCL/std/stdpar/execution
%{_includedir}/%{upstream_name}/hipSYCL/std/stdpar/numeric

# cmake
%{_libdir}/cmake/hipSYCL/*
%{_libdir}/cmake/OpenSYCL/*
%{_libdir}/cmake/%{upstream_name}/*

# libs
%{_libdir}/libacpp-clang.so
%{_libdir}/libacpp-common.so
%{_libdir}/libacpp-rt.so
%{_libdir}/libllvm-to-amdgpu.so
%{_libdir}/libllvm-to-backend.so

%changelog
* Sat Nov 25 2023 Tom Rix <trix@redhat.com> - 23.10.0-1
- Initial package

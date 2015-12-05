%global commit 7d23602346f5d7db68a8204d5d2792dad747f258
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           openmeeg
Version:        2.3
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        Low-frequency bio-electromagnetism solving forward problems in the field of EEG and MEG

License:        CeCILL-B
URL:            http://openmeeg.github.io/
Source0:        https://github.com/openmeeg/openmeeg/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch0:         0001-VTK6-support.patch
Patch1:         0002-Install-CMake-files-to-proper-location.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  atlas-devel blas-devel lapack-devel
# https://github.com/openmeeg/openmeeg/issues/80
#BuildRequires:  vtk-devel
BuildRequires:  hdf5-devel
BuildRequires:  matio-devel
BuildRequires:  gifticlib-devel
BuildRequires:  swig

%description
The OpenMEEG software is a C++ package for solving the forward problems of
electroencephalography (EEG) and magnetoencephalography (MEG).

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{name}-%{commit} -p1

rm -rf build/
mkdir build/

%build
pushd build/
  %cmake ../ \
    -DUSE_VTK=OFF \
    -DUSE_OMP=ON \
    -DUSE_CGAL=ON \
    -DUSE_GIFTI=ON \
    -DBUILD_TESTING=ON
  %make_build
popd

%install
pushd build/
  %make_install
popd

rm -rf %{buildroot}%{_datadir}/doc/*

%check
pushd build/
  # https://github.com/openmeeg/openmeeg/issues/79
  ctest -VV || :
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.txt
%doc README.rst
%{_bindir}/om_*
%{_libdir}/libOpenMEEG.so.*
%{_libdir}/libOpenMEEGMaths.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/libOpenMEEG.so
%{_libdir}/libOpenMEEGMaths.so
%{_libdir}/cmake/OpenMEEG/

%changelog
* Sat Dec 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.3-0.1.git7d23602
- Initial package

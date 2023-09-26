%define module_dir extra

Summary: Driver for mpi3mr-module
Name: mpi3mr-module
Version: 8.6.1.0.0
Release: 0%{?dist}
License: GPL-2.0-or-later

# https://www.broadcom.com/support/download-search?pg=Storage+Adapters,+Controllers,+and+ICs&pf=Storage+Adapters,+Controllers,+and+ICs&pn=MegaRAID+9670W-16i&pa=&po=&dk=&pl=&l=false
Source: mpi3mr-%{version}-src.tar.gz

Patch0: 0001-bsg-lib-pre-5.0-API.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
Broadcom mpi3mr device drivers for the Linux Kernel version %{kernel_version}.

%prep
%autosetup -n mpi3mr

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{kernel_version}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Wed Sep 20 2023 Yann Dirson <yann.dirson@vates.tech> - 8.6.1.0.0-0
- Initial beta packaging

%global milestone .0rc1
%global drv_vendor OpenDaylight
%global pkgname networking-odl
%global srcname networking_odl
%global docpath doc/build/html

# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1
%{!?dlrn: %global repo_bootstrap 1}

%global common_desc \
This package contains %{drv_vendor} networking driver for OpenStack Neutron.

Name:           python-%{pkgname}
Epoch:          1
Version:        14.0.0
Release:        0.1%{?milestone}%{?dist}
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{upstream_version}.tar.gz

#
# patches_base=14.0.0.0rc1
#

BuildArch:      noarch

BuildRequires:  git

%description
%{common_desc}

%package -n python%{pyver}-%{pkgname}
Summary:        %{drv_vendor} OpenStack Neutron driver
%{?python_provide:%python_provide python%{pyver}-%{pkgname}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-mock
#BuildRequires:  python%{pyver}-neutron-tests
%if 0%{?with_doc}
BuildRequires:  python%{pyver}-openstackdocstheme
%endif
#BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-testtools

Requires:       openstack-ceilometer-common >= 11.0.0
Requires:       openstack-neutron-ml2
Requires:       openstack-neutron-lbaas >= 1:13.0.0
Requires:       openstack-neutron >= 1:13.0.0
Requires:       python%{pyver}-babel >= 2.5.3
%if 0%{?repo_bootstrap} == 0
Requires:       python%{pyver}-networking-bgpvpn >= 8.0.0
%endif
Requires:       python%{pyver}-networking-l2gw >= 12.0.0
Requires:       python%{pyver}-networking-sfc >= 6.0.0
Requires:       python%{pyver}-pbr >= 3.1.1

# Handle python2 exception
%if %{pyver} == 2
Requires:  python-websocket-client >= 0.47.0
%else
Requires:  python%{pyver}-websocket-client >= 0.47.0
%endif
Requires:       python%{pyver}-stevedore >= 1.28.0
Requires:       python%{pyver}-neutron-lib >= 1.18.0
Requires:       python%{pyver}-debtcollector

%description -n python%{pyver}-%{pkgname}
%{common_desc}


%prep
%autosetup -n %{pkgname}-%{upstream_version} -S git
# Remove gate hooks
rm -rf %{srcname}/tests/contrib

%build
%{pyver_build}

%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-%{pyver} -W -b html doc/source %{docpath}
rm -rf %{docpath}/.{buildinfo,doctrees}
%endif

%check
export PYTHON=%{pyver_bin}
#stestr-%{pyver} run


%install
%{pyver_install}

# Move config file to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron/plugins/ml2
mv %{buildroot}/usr/etc/neutron/* %{buildroot}%{_sysconfdir}/neutron/plugins/ml2
chmod 640 %{buildroot}%{_sysconfdir}/neutron/plugins/*/*.ini

%files -n python%{pyver}-%{pkgname}
%license LICENSE
%if 0%{?with_doc}
%doc %{docpath}
%endif
%{_bindir}/neutron-odl-ovs-hostconfig
%{_bindir}/neutron-odl-analyze-journal-logs
%{pyver_sitelib}/%{srcname}
%{pyver_sitelib}/%{srcname}-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/ml2/*.ini

%changelog
* Fri Mar 22 2019 RDO <dev@lists.rdoproject.org> 1:14.0.0-0.1.0rc1
- Update to 14.0.0.0rc1


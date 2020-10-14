%global drv_vendor OpenDaylight
%global pkgname networking-odl
%global srcname networking_odl
%global docpath doc/build/html


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global common_desc \
This package contains %{drv_vendor} networking driver for OpenStack Neutron.

Name:           python-%{pkgname}
Epoch:          1
Version:        17.0.0
Release:        1%{?dist}
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{upstream_version}.tar.gz

#

BuildArch:      noarch

BuildRequires:  git

%description
%{common_desc}

%package -n python3-%{pkgname}
Summary:        %{drv_vendor} OpenStack Neutron driver
%{?python_provide:%python_provide python3-%{pkgname}}

BuildRequires:  python3-devel
BuildRequires:  python3-mock
#BuildRequires:  python3-neutron-tests
%if 0%{?with_doc}
BuildRequires:  python3-openstackdocstheme
%endif
#BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-config
BuildRequires:  python3-pbr
BuildRequires:  python3-sphinx
BuildRequires:  python3-stestr
BuildRequires:  python3-testtools

Requires:       openstack-ceilometer-common >= 11.0.0
Requires:       openstack-neutron-ml2
Requires:       openstack-neutron >= 1:16.0.0
# NOTE(jpena): networking-bgpvpn requires networking-odl, so we need to avoid
# the circular dependency
#Requires:       python3-networking-bgpvpn >= 8.0.0
Requires:       python3-networking-l2gw >= 12.0.0
Requires:       python3-networking-sfc >= 10.0.0
Requires:       python3-pbr >= 4.0.0
Requires:  python3-websocket-client >= 0.47.0
Requires:       python3-stevedore >= 1.28.0
Requires:       python3-neutron-lib >= 2.0.0
Requires:       python3-debtcollector

%description -n python3-%{pkgname}
%{common_desc}


%prep
%autosetup -n %{pkgname}-%{upstream_version} -S git
# Remove gate hooks
rm -rf %{srcname}/tests/contrib

%build
%{py3_build}

%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-3 -W -b html doc/source %{docpath}
rm -rf %{docpath}/.{buildinfo,doctrees}
%endif

%check
export PYTHON=%{__python3}
#stestr-3 run


%install
%{py3_install}

# Move config file to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron/plugins/ml2
mv %{buildroot}/usr/etc/neutron/* %{buildroot}%{_sysconfdir}/neutron/plugins/ml2
chmod 640 %{buildroot}%{_sysconfdir}/neutron/plugins/*/*.ini

%files -n python3-%{pkgname}
%license LICENSE
%if 0%{?with_doc}
%doc %{docpath}
%endif
%{_bindir}/neutron-odl-ovs-hostconfig
%{_bindir}/neutron-odl-analyze-journal-logs
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/ml2/*.ini

%changelog
* Wed Oct 14 2020 RDO <dev@lists.rdoproject.org> 1:17.0.0-1
- Update to 17.0.0

* Fri Sep 25 2020 RDO <dev@lists.rdoproject.org> 1:17.0.0-0.1.0rc1
- Update to 17.0.0.0rc1


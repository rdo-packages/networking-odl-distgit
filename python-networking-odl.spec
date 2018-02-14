%global drv_vendor OpenDaylight
%global pkgname networking-odl
%global srcname networking_odl
%global docpath doc/build/html

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pkgname}
Epoch:          1
Version:        XXX
Release:        XXX
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-mock
#BuildRequires:  python2-neutron-tests
BuildRequires:  python2-openstackdocstheme
#BuildRequires:  python2-oslotest
BuildRequires:  python2-oslo-config
BuildRequires:  python2-pbr
BuildRequires:  python2-sphinx
BuildRequires:  python2-testrepository
BuildRequires:  python2-testtools

Requires:       openstack-neutron-ml2
Requires:       python2-babel
Requires:       python2-pbr
Requires:       python2-websocket-client
Requires:       python2-stevedore
Requires:       python2-neutron-lib >= 1.13.0
Requires:       python2-debtcollector

%description
This package contains %{drv_vendor} networking driver for OpenStack Neutron.


%prep
%autosetup -n %{pkgname}-%{upstream_version} -S git
# Remove gate hooks
rm -rf %{srcname}/tests/contrib

%build
rm requirements.txt test-requirements.txt
%{__python2} setup.py build
%{__python2} setup.py build_sphinx -b html
rm %{docpath}/.buildinfo


#%check
#%{__python2} setup.py testr


%install
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py install --skip-build --root %{buildroot}

# Move config file to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron/plugins/ml2
mv %{buildroot}/usr/etc/neutron/* %{buildroot}%{_sysconfdir}/neutron/plugins/ml2
chmod 640 %{buildroot}%{_sysconfdir}/neutron/plugins/*/*.ini


%files
%license LICENSE
%doc %{docpath}
%{_bindir}/neutron-odl-ovs-hostconfig
%{_bindir}/neutron-odl-analyze-journal-logs
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/ml2/*.ini

%changelog

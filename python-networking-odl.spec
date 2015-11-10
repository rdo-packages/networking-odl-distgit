%global drv_vendor OpenDaylight
%global pkgname networking-odl
%global srcname networking_odl
%global docpath doc/build/html

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pkgname}
Version:        1.0.1
Release:        1%{?dist}
Epoch:          1
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://pypi.python.org/packages/source/n/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-mock
BuildRequires:  python-neutron-tests
BuildRequires:  python-oslo-sphinx
#BuildRequires:  python-oslotest
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-testrepository
BuildRequires:  python-testtools
BuildRequires:  python-webtest

Requires:       openstack-neutron-ml2
Requires:       python-babel
Requires:       python-pbr


%description
This package contains %{drv_vendor} networking driver for OpenStack Neutron.


%prep
%setup -q -n %{pkgname}-%{upstream_version}


%build
rm requirements.txt test-requirements.txt
%{__python2} setup.py build
%{__python2} setup.py build_sphinx
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
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/ml2/*.ini


%changelog
* Tue Nov 10 2015 Ihar Hrachyshka <ihrachys@redhat.com> 1:1.0.1-1
- Initial build

%global drv_vendor OpenDaylight
%global pkgname networking-odl
%global srcname networking_odl
%global docpath doc/build/html

%{!?upstream_version: %global upstream_version %{commit}}
%global commit f95b3204f8adc3f6942031c8c0d7c114e51e3318
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

Name:           python-%{pkgname}
Epoch:          1
Version:        2.0.1
Release:        0.1%{?alphatag}%{?dist}
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://github.com/openstack/%{pkgname}/archive/%{commit}.tar.gz#/%{pkgname}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-mock
#BuildRequires:  python-neutron-tests
BuildRequires:  python-oslo-sphinx
#BuildRequires:  python-oslotest
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-testrepository
BuildRequires:  python-testtools
BuildRequires:  python-webtest
BuildRequires:  git

Requires:       openstack-neutron-ml2
Requires:       python-babel
Requires:       python-pbr


%description
This package contains %{drv_vendor} networking driver for OpenStack Neutron.


%prep
%autosetup -n %{pkgname}-%{upstream_version} -S git


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
%{_bindir}/neutron-odl-ovs-hostconfig
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/ml2/*.ini

%changelog
* Wed Oct 5 2016 Alfredo Moralejo <amoralej@redhat.com> - 1:2.0.1-0.1.f95b320git
- Update to post 2.0.0 (f95b3204f8adc3f6942031c8c0d7c114e51e3318)

* Wed Jun 29 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1:2.0.0-1
- Upstream 2.0.0


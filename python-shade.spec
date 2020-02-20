# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver 3
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global srcname shade

%global common_desc shade is a simple client library for operating OpenStack clouds.

Name:           python-%{srcname}
Version:        1.32.0
Release:        1%{?dist}
Summary:        Python module for operating OpenStack clouds

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/shade
Source0:        https://tarballs.openstack.org/shade/shade-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-devel

# test-requirements.txt
BuildRequires: python%{pyver}-mock
BuildRequires: python%{pyver}-betamax

# requirements.txt
BuildRequires:  python%{pyver}-six
BuildRequires:  python%{pyver}-jsonpatch
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-munch
BuildRequires:  python%{pyver}-os-client-config
BuildRequires:  python%{pyver}-requestsexceptions
BuildRequires:  python%{pyver}-jmespath
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios
%if %{pyver} == 2
BuildRequires:  python-decorator
BuildRequires:  python-netifaces
BuildRequires:  python-dogpile-cache
BuildRequires:  python-ipaddress
BuildRequires:  python-requests-mock
%else
BuildRequires:  python%{pyver}-decorator
BuildRequires:  python%{pyver}-netifaces
BuildRequires:  python%{pyver}-dogpile-cache
BuildRequires:  python%{pyver}-requests-mock
%endif

%description
%{common_desc}

%package -n python%{pyver}-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{pyver}-%{srcname}}
Requires:       python%{pyver}-iso8601                  >= 0.1.11
Requires:       python%{pyver}-jmespath                 >= 0.9.0
Requires:       python%{pyver}-jsonpatch                >= 1.16
Requires:       python%{pyver}-keystoneauth1            >= 3.3.0
Requires:       python%{pyver}-munch                    >= 2.1.0
Requires:       python%{pyver}-os-client-config         >= 1.28.0
Requires:       python%{pyver}-openstacksdk             >= 0.15.0
Requires:       python%{pyver}-pbr                      >= 2.0.0
Requires:       python%{pyver}-requestsexceptions       >= 1.2.0
Requires:       python%{pyver}-six                      >= 1.10.0
%if %{pyver} == 2
Requires:       python-dogpile-cache             >= 0.6.2
Requires:       python-futures                   >= 3.0
Requires:       python-ipaddress                 >= 1.0.16
Requires:       python-decorator                 >= 3.4.0
Requires:       python-netifaces                 >= 0.10.4
%else
Requires:       python%{pyver}-dogpile-cache            >= 0.6.2
Requires:       python%{pyver}-decorator                >= 3.4.0
Requires:       python%{pyver}-netifaces                >= 0.10.4
%endif

%description -n python%{pyver}-%{srcname}
%{common_desc}

%prep
%autosetup -n %{srcname}-%{upstream_version}

%build
%pyver_build

%check
#PYTHON=%{pyver_bin} %{pyver_bin} setup.py testr

%install
%pyver_install
mv $RPM_BUILD_ROOT%{_bindir}/shade-inventory \
        $RPM_BUILD_ROOT%{_bindir}/shade-inventory-%{pyver}
ln -s shade-inventory-%{pyver} \
        $RPM_BUILD_ROOT%{_bindir}/shade-inventory

%files -n python%{pyver}-%{srcname}
%license LICENSE
%doc README.rst AUTHORS
%{pyver_sitelib}/shade*

%{_bindir}/shade-inventory-%{pyver}
%{_bindir}/shade-inventory

%changelog
* Thu Oct 10 2019 RDO <dev@lists.rdoproject.org> 1.32.0-1
- Update to 1.32.0


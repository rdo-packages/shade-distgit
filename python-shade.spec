
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global srcname shade

%global common_desc shade is a simple client library for operating OpenStack clouds.

Name:           python-%{srcname}
Version:        1.33.0
Release:        1%{?dist}
Summary:        Python module for operating OpenStack clouds

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/shade
Source0:        https://tarballs.openstack.org/shade/shade-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python3-pbr
BuildRequires:  python3-devel

# test-requirements.txt
BuildRequires: python3-mock
BuildRequires: python3-betamax

# requirements.txt
BuildRequires:  python3-six
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-munch
BuildRequires:  python3-os-client-config
BuildRequires:  python3-requestsexceptions
BuildRequires:  python3-jmespath
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-decorator
BuildRequires:  python3-netifaces
BuildRequires:  python3-dogpile-cache
BuildRequires:  python3-requests-mock

%description
%{common_desc}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
Requires:       python3-jmespath                 >= 0.9.0
Requires:       python3-keystoneauth1            >= 3.3.0
Requires:       python3-munch                    >= 2.1.0
Requires:       python3-os-client-config         >= 1.28.0
Requires:       python3-openstacksdk             >= 0.15.0
Requires:       python3-pbr                      >= 2.0.0
Requires:       python3-requestsexceptions       >= 1.2.0
Requires:       python3-six                      >= 1.10.0
Requires:       python3-dogpile-cache            >= 0.6.2
Requires:       python3-decorator                >= 3.4.0
Requires:       python3-netifaces                >= 0.10.4

%description -n python3-%{srcname}
%{common_desc}

%prep
%autosetup -n %{srcname}-%{upstream_version}

%build
%py3_build

%check
#PYTHON=%{__python3} %{__python3} setup.py testr

%install
%py3_install
mv $RPM_BUILD_ROOT%{_bindir}/shade-inventory \
        $RPM_BUILD_ROOT%{_bindir}/shade-inventory-3
ln -s shade-inventory-3 \
        $RPM_BUILD_ROOT%{_bindir}/shade-inventory

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst AUTHORS
%{python3_sitelib}/shade*

%{_bindir}/shade-inventory-3
%{_bindir}/shade-inventory

%changelog
* Fri Sep 25 2020 RDO <dev@lists.rdoproject.org> 1.33.0-1
- Update to 1.33.0


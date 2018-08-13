# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pydefault 3
%else
%global pydefault 2
%endif

%global pydefault_bin python%{pydefault}
%global pydefault_sitelib %python%{pydefault}_sitelib
%global pydefault_install %py%{pydefault}_install
%global pydefault_build %py%{pydefault}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global srcname shade

%global common_desc shade is a simple client library for operating OpenStack clouds.

Name:           python-%{srcname}
Version:        XXX
Release:        XXX
Summary:        Python module for operating OpenStack clouds

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/shade
Source0:        https://tarballs.openstack.org/shade/shade-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python%{pydefault}-pbr
BuildRequires:  python%{pydefault}-devel

# test-requirements.txt
BuildRequires: python%{pydefault}-mock
BuildRequires: python%{pydefault}-betamax

# requirements.txt
BuildRequires:  python%{pydefault}-six
BuildRequires:  python%{pydefault}-jsonpatch
BuildRequires:  python%{pydefault}-keystoneauth1
BuildRequires:  python%{pydefault}-munch
BuildRequires:  python%{pydefault}-os-client-config
BuildRequires:  python%{pydefault}-requestsexceptions
BuildRequires:  python%{pydefault}-jmespath
BuildRequires:  python%{pydefault}-testrepository
BuildRequires:  python%{pydefault}-testscenarios
%if %{pydefault} == 2
BuildRequires:  python-decorator
BuildRequires:  python-netifaces
BuildRequires:  python-dogpile-cache
BuildRequires:  python-ipaddress
BuildRequires:  python-requests-mock
%else
BuildRequires:  python%{pydefault}-decorator
BuildRequires:  python%{pydefault}-netifaces
BuildRequires:  python%{pydefault}-dogpile-cache
BuildRequires:  python%{pydefault}-requests-mock
%endif

%description
%{common_desc}

%package -n python%{pydefault}-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{pydefault}-%{srcname}}
Requires:       python%{pydefault}-iso8601                  >= 0.1.11
Requires:       python%{pydefault}-jmespath                 >= 0.9.0
Requires:       python%{pydefault}-jsonpatch                >= 1.16
Requires:       python%{pydefault}-keystoneauth1            >= 3.3.0
Requires:       python%{pydefault}-munch                    >= 2.1.0
Requires:       python%{pydefault}-os-client-config         >= 1.28.0
Requires:       python%{pydefault}-openstacksdk             >= 0.15.0
Requires:       python%{pydefault}-pbr                      >= 2.0.0
Requires:       python%{pydefault}-requestsexceptions       >= 1.2.0
Requires:       python%{pydefault}-six                      >= 1.10.0
%if %{pydefault} == 2
Requires:       python-dogpile-cache             >= 0.6.2
Requires:       python-futures                   >= 3.0
Requires:       python-ipaddress                 >= 1.0.16
Requires:       python-decorator                 >= 3.4.0
Requires:       python-netifaces                 >= 0.10.4
%else
Requires:       python%{pydefault}-dogpile-cache            >= 0.6.2
Requires:       python%{pydefault}-decorator                >= 3.4.0
Requires:       python%{pydefault}-netifaces                >= 0.10.4
%endif

%description -n python%{pydefault}-%{srcname}
%{common_desc}

%prep
%autosetup -n %{srcname}-%{upstream_version}

%build
%pydefault_build

%check
#PYTHON=%{pydefault_bin} %{pydefault_bin} setup.py testr

%install
%pydefault_install
mv $RPM_BUILD_ROOT%{_bindir}/shade-inventory \
        $RPM_BUILD_ROOT%{_bindir}/shade-inventory-%{pydefault}
ln -s shade-inventory-%{pydefault} \
        $RPM_BUILD_ROOT%{_bindir}/shade-inventory

%files -n python%{pydefault}-%{srcname}
%license LICENSE
%doc README.rst AUTHORS
%{pydefault_sitelib}/shade*

%{_bindir}/shade-inventory-%{pydefault}
%{_bindir}/shade-inventory

%changelog

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# TODO: Explain why python3 is disabled in Fedora
%if 0%{?fedora}
%global with_python3 0
%endif

%if 0%{?__python2:1}
%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print("%s.%s" % (sys.version_info.major,sys.version_info.minor))')}
%else
%{!?python2_shortver: %global python3_shortver 2.x}
%endif

%if 0%{?__python3:1}
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print("%s.%s" % (sys.version_info.major,sys.version_info.minor))')}
%else
%{!?python3_shortver: %global python3_shortver 3.x}
%endif

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
BuildRequires:  python-pbr

# test-requirements.txt
BuildRequires: python-fixtures
BuildRequires: python-mock
BuildRequires: python-subunit
BuildRequires: python-oslotest
BuildRequires: python-requests-mock
BuildRequires: python-testscenarios
BuildRequires: python-testtools
BuildRequires: python-stestr
BuildRequires: python-futures

# requirements.txt
BuildRequires:  python-dogpile-cache
BuildRequires:  python-six
BuildRequires:  python-ipaddress
BuildRequires:  python-jsonpatch
BuildRequires:  python-decorator
BuildRequires:  python-munch
BuildRequires:  python-keystoneauth1
BuildRequires:  python-os-client-config
BuildRequires:  python2-requestsexceptions
BuildRequires:  python-netifaces
BuildRequires:  python2-jmespath
BuildRequires:  python-requests-mock


%description
%{common_desc}

%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}

BuildRequires:  python2-devel

Requires:       python-decorator                >= 3.4.0
Requires:       python-dogpile-cache            >= 0.6.2
Requires:       python-futures                  >= 3.0
Requires:       python-ipaddress                >= 1.0.16
Requires:       python-iso8601                  >= 0.1.11
Requires:       python-jmespath                 >= 0.9.0
Requires:       python-jsonpatch                >= 1.1
Requires:       python-keystoneauth1            >= 3.3.0
Requires:       python-munch                    >= 2.0.2
Requires:       python-netifaces                >= 0.10.4
Requires:       python-os-client-config         >= 1.28.0
Requires:       python-pbr                      >= 2.0.0
Requires:       python-requestsexceptions       >= 1.2.0
Requires:       python-six                      >= 1.10.0

%description -n python2-%{srcname}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

BuildRequires:  python3-devel

Requires:       python3-decorator               >= 3.4.0
Requires:       python3-dogpile-cache           >= 0.6.2
Requires:       python3-iso8601                 >= 0.1.11
Requires:       python3-jmespath                >= 0.9.0
Requires:       python3-jsonpatch               >= 1.1
Requires:       python3-keystoneauth1           >= 3.3.0
Requires:       python3-munch                   >= 2.0.2
Requires:       python3-netifaces               >= 0.10.4
Requires:       python3-os-client-config        >= 1.28.0
Requires:       python3-pbr                     >= 2.0.0
Requires:       python3-requestsexceptions      >= 1.2.0
Requires:       python3-six                     >= 1.10.0

%description -n python3-%{srcname}
%{common_desc}
%endif

%prep
%autosetup -n %{srcname}-%{upstream_version}
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%install
%py2_install
mv $RPM_BUILD_ROOT%{_bindir}/shade-inventory \
        $RPM_BUILD_ROOT%{_bindir}/shade-inventory-%{python2_shortver}
%if 0%{?with_python3}
%py3_install
mv $RPM_BUILD_ROOT%{_bindir}/shade-inventory \
        $RPM_BUILD_ROOT%{_bindir}/shade-inventory-%{python3_shortver}
%endif

# handle symlinking of unversioned binary
%if 0%{?with_python3}
ln -s shade-inventory-%{python3_shortver} \
        $RPM_BUILD_ROOT%{_bindir}/shade-inventory
%else
ln -s shade-inventory-%{python2_shortver} \
        $RPM_BUILD_ROOT%{_bindir}/shade-inventory
%endif

%files -n python2-%{srcname}
%license LICENSE
%doc README.rst AUTHORS
%{python2_sitelib}/shade*

%{_bindir}/shade-inventory-%{python2_shortver}
%if ! 0%{?with_python3}
%{_bindir}/shade-inventory
%endif

%if 0%{?with_python3}
%files -n python3-%{srcname}
%license LICENSE
%doc README.rst AUTHORS
%{python3_sitelib}/shade*

%{_bindir}/shade-inventory-%{python3_shortver}
%{_bindir}/shade-inventory
%endif

%changelog

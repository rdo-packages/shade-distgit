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
BuildRequires:  python2-devel

# test-requirements.txt
BuildRequires: python-mock
BuildRequires: python-testrepository
BuildRequires: python-testscenarios
BuildRequires: python-betamax

# requirements.txt
BuildRequires:  python-dogpile-cache
BuildRequires:  python-designateclient
BuildRequires:  python-ironicclient
BuildRequires:  python-glanceclient
BuildRequires:  python-keystoneclient
BuildRequires:  python-novaclient
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

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3

%description
%{common_desc}

%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
Requires:       python-dogpile-cache            >= 0.6.2
Requires:       python-designateclient          >= 2.1.0
Requires:       python-ironicclient             >= 1.11.0
Requires:       python-glanceclient             >= 1.0.0
Requires:       python-keystoneclient           >= 1:3.8.0
Requires:       python-novaclient               >= 1:7.1.0
Requires:       python-six
Requires:       python-ipaddress
Requires:       python-jsonpatch
Requires:       python-decorator
Requires:       python-munch
Requires:       python-keystoneauth1            >= 2.20.0
Requires:       python-os-client-config         >= 1.27.0
Requires:       python-requestsexceptions       >= 1.2.0
Requires:       python-netifaces
Requires:       python-jmespath

%description -n python2-%{srcname}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
Requires:       python3-dogpile-cache           >= 0.6.2
Requires:       python3-designateclient         >= 2.1.0
Requires:       python3-ironicclient            >= 1.11.0
Requires:       python3-glanceclient            >= 1.0.0
Requires:       python3-keystoneclient          >= 1:3.8.0
Requires:       python3-novaclient              >= 1:7.1.0
Requires:       python3-six
Requires:       python3-ipaddress
Requires:       python3-jsonpatch
Requires:       python3-decorator
Requires:       python3-munch
Requires:       python3-keystoneauth1           >= 2.20.0
Requires:       python3-os-client-config        >= 1.27.0
Requires:       python3-requestsexceptions      >= 1.2.0
Requires:       python3-netifaces

%description -n python3-%{srcname}
%{common_desc}
%endif

%prep
%autosetup -n %{srcname}-%{upstream_version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%check
#%{__python2} setup.py testr
# cleanup testrepository
#rm -rf .testrepository
#%if 0%{?with_python3}
#%{__python3} setup.py testr
#%endif

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

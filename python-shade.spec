%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xbba3b1e67a7303dd1769d34595bf2e4d09004514

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order sphinx openstackdocstheme

%global srcname shade

%global common_desc shade is a simple client library for operating OpenStack clouds.

Name:           python-%{srcname}
Version:        1.33.0
Release:        2%{?dist}
Summary:        Python module for operating OpenStack clouds

License:        Apache-2.0
URL:            https://pypi.python.org/pypi/shade
Source0:        https://tarballs.openstack.org/shade/shade-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/shade/shade-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
%{common_desc}

%package -n python3-%{srcname}
Summary:        %{summary}

Requires:       python3-munch >= 2.1.0

%description -n python3-%{srcname}
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{srcname}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%check
#PYTHON=%{__python3} %{__python3} setup.py testr

%install
%pyproject_install
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
* Fri Mar 15 2024 RDO <dev@lists.rdoproject.org> 1.33.0-2
- Rebuild 1.33.0 in Caracal


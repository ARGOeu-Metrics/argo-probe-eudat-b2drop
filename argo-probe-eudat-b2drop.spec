Name:		argo-probe-eudat-b2drop
Version:	1.0
Release:	1%{?dist}
Summary:	Monitoring Metrics for B2DROP 
License:	GPLv3+
Packager:	Kyriakos Gkinis <kyrginis@admin.grnet.gr>

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

Requires:	python3

%description
Monitoring metrics to check functionality of B2DROP service 

%prep
%setup -q

%define _unpackaged_files_terminate_build 0 

%install

install -d %{buildroot}/%{_libexecdir}/argo/probes/eudat-b2drop
install -m 755 b2drop_api.py %{buildroot}/%{_libexecdir}/argo/probes/eudat-b2drop/b2drop_api.py
install -m 755 b2drop.py %{buildroot}/%{_libexecdir}/argo/probes/eudat-b2drop/b2drop.py
install -m 755 probes.py %{buildroot}/%{_libexecdir}/argo/probes/eudat-b2drop/probes.py


%files
%dir /%{_libexecdir}/argo
%dir /%{_libexecdir}/argo/probes/
%dir /%{_libexecdir}/argo/probes/eudat-b2drop

%attr(0755,root,root) /%{_libexecdir}/argo/probes/eudat-b2drop/b2drop_api.py
%attr(0755,root,root) /%{_libexecdir}/argo/probes/eudat-b2drop/b2drop.py
%attr(0644,root,root) /%{_libexecdir}/argo/probes/eudat-b2drop/probes.py

%pre

%changelog
* Thu Feb 6 2025 Themis Zamani <themiszamani@gmail.com> - 0.9-4
- Initial version of the package

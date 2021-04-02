%define _topdir		%(echo $HOME)/rpmbuild-%{name}
%define _conf_dir       %{_sysconfdir}/%{name}
Name:           redis
Version:        6.2.1
Release:        2%{?dist}
Summary:        A persistent key-value database

License:        BSD and MIT
URL:            http://redis.io
Source0:        https://download.redis.io/releases/%{name}-%{version}.tar.gz


BuildRequires: gcc
BuildRequires: openssl-devel
BuildRequires: systemd-devel

%description
%{name} is an advanced key-value store. It is similar to memcached but the dataset
is not volatile, and values can be strings, exactly like in memcached,
but also lists, sets, and ordered sets. All this data types can be manipulated
with atomic operations to push/pop elements, add/remove elements, perform server
side union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.


%prep
%autosetup


%build
make BUILD_TLS=yes USE_SYSTEMD=yes


%install
install -Dpm0755 src/%{name}-server     %{buildroot}%{_sbindir}/%{name}-server
install -Dpm0755 src/%{name}-sentinel   %{buildroot}%{_sbindir}/%{name}-sentinel
install -Dpm0755 src/%{name}-cli        %{buildroot}%{_sbindir}/%{name}-cli
install -Dpm0755 src/%{name}-benchmark  %{buildroot}%{_sbindir}/%{name}-benchmark
install -Dpm0640 redis.conf             %{buildroot}%{_conf_dir}/redis.conf
install -Dpm0640 sentinel.conf		%{buildroot}%{_conf_dir}/sentinel.conf

%files
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}-sentinel
%{_sbindir}/%{name}-cli
%{_sbindir}/%{name}-benchmark
%{_conf_dir}/redis.conf
%{_conf_dir}/sentinel.conf


%changelog
* Fri Apr 02 2021 jethigh
- Added BuildRequires
- Defined _topdir to point custom rpmbuild direcotry name 

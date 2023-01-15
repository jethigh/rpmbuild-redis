%global _topdir     %(echo $HOME)
%global _conf_dir   %{_sysconfdir}/%{name}
# Build variables
%global tls_flag    BUILD_TLS=yes
%global sysd_flag   USE_SYSTEMD=yes
%global make_flags  %{?tls_flag} %{?sysd_flag}


Name:           redis
Version:        7.0.7
Release:        1%{?dist}
Summary:        A persistent key-value database

License:        BSD and MIT
URL:            https://github.com
Source0:        https://github.com/redis/redis/archive/%{version}.tar.gz
Source1:        %{name}.service

Requires:       systemd
BuildRequires:  gcc
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel


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
make %{make_flags}


%install
install -Dpm0755 src/%{name}-server     %{buildroot}%{_bindir}/%{name}-server
install -Dpm0755 src/%{name}-sentinel   %{buildroot}%{_bindir}/%{name}-sentinel
install -Dpm0755 src/%{name}-cli        %{buildroot}%{_bindir}/%{name}-cli
install -Dpm0755 src/%{name}-benchmark  %{buildroot}%{_bindir}/%{name}-benchmark
install -Dpm0755 src/%{name}-check-aof  %{buildroot}%{_bindir}/%{name}-check-aof
install -Dpm0755 src/%{name}-check-rdb  %{buildroot}%{_bindir}/%{name}-check-rdb
install -Dpm0640 redis.conf             %{buildroot}%{_conf_dir}/redis.conf
install -Dpm0640 sentinel.conf		%{buildroot}%{_conf_dir}/sentinel.conf
install -Dpm0640 %{SOURCE1} 		%{buildroot}%{_unitdir}/%{name}.service


%files
%{_bindir}/%{name}-server
%{_bindir}/%{name}-sentinel
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-benchmark
%{_bindir}/%{name}-check-aof
%{_bindir}/%{name}-check-rdb
%{_conf_dir}/%{name}.conf
%{_conf_dir}/sentinel.conf
%{_unitdir}/%{name}.service


%pre
# Add redis user and group
groupadd -r %{name} &> /dev/null
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin -c 'Redis Database Server' %{name} &> /dev/null

# Make working directory
mkdir -p /var/lib/%{name}
chown -R redis:redis /var/lib/%{name}


%post
# Change config files ownership
chown %{name} %{_conf_dir}/%{name}.conf
chown %{name} %{_conf_dir}/sentinel.conf

# Change redis.conf to supervised
sed -i 's/# supervised auto/supervised auto/g' %{_conf_dir}/%{name}.conf

# Change working directory
sed -i 's/dir .\//dir \/var\/lib\/%{name}\//g' %{_conf_dir}/%{name}.conf

# Manage systemd service
%systemd_post %{name}.service


%preun
# Manage systemd service
%systemd_preun %{name}.service


%postun
# Remove config, and user
rm -r %{_conf_dir}
userdel %{name}

# Change working dir permisions to root
chown -R root:root /var/lib/%{name}

# Manage systemd service
%systemd_postun_with_restart %{name}.service


%changelog
* Sun Jan 15 2023 jethigh
- Version 7.0.7 of redis sources
- Added repair tools

* Tue Apr 20 2021 jethigh
- Creating redis group and user
- Removing added group and user on uninstall
- Adding systemd unit file
- Removinf systemd unit file on uninstall
- Enablilng redis service 

* Fri Apr 02 2021 jethigh
- Added BuildRequires
- Defined _topdir to point custom rpmbuild direcotry name 
- Added macros for make flags
- Defined macroc moved to top
- Deleting config dir after uninstall

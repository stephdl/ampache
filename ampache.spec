%define __requires_exclude ^(pear\\(Auth.*|pear\\(PHPUnit.*|pear\\(config.*)$

Name:           ampache
Version:        3.8.2
Release:        1%{?dist}
Summary:        Web-based MP3/Ogg/RM/Flac/WMA/M4A manager
License:        AGPLv3+
Group:          Networking/WWW
URL:            http://www.ampache.org
Source0:        https://github.com/ampache/ampache/releases/download/%{version}/%{name}-%{version}_all.zip
Requires:	php
Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-mysql
Requires:       php-gd
BuildArch:      noarch

%description
Ampache is a Web-based MP3/Ogg/RM/Flac/WMA/M4A manager.
It allows you to view, edit, and play your audio files via HTTP/IceCast/Mpd
or Moosic. It has support for downsampling, playlists, artist,
and album views, album art, random play, song play tracking, user themes,
and remote catalogs using XML-RPC.

%prep
mkdir %{name}-%{version}
cd %{name}-%{version}
unzip %{SOURCE0}

%build
# Nothing to do!!

%install
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -r %{name}-%{version}/* %{buildroot}%{_datadir}/%{name}

# apache configuration
install -d -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf<<EOF
# Ampache configuration

Alias /%{name} %{_datadir}/%{name}
<Directory %{_datadir}/%{name}>
    Require all granted
    php_admin_value post_max_size 110M
    php_admin_value upload_max_filesize 100M
</Directory>
EOF

%files
%doc %{name}-%{version}/docs/*
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/config
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/channel
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/rest
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/play


%changelog
* Sat Feb 11 2017 stephane de Labrusse <stephdl@de-labrusse.fr> 3.8.2-1-el7
- First release of ampache

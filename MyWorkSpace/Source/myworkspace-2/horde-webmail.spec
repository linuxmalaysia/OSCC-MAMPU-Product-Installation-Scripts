#
%define contentdir /usr/share/
%define apacheuser apache
%define apachegroup apache

Summary: Horde Webmail
Name: horde-webmail
Version: 1.2.2
Release: 1
License: LGPL
Group: Applications/Internet
Vendor:   OSCC MAMPU
Packager: Harisfazillah Jamel <haris@oscc.org.my>
URL: http://www.horde.org/
### ftp://ftp.horde.org/pub/horde-webmail/horde-webmail-1.1.3.tar.gz
Source: ftp://ftp.horde.org/pub/horde-webmail/horde-webmail-%{version}.tar.gz
Source1: webmail.conf
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
AutoReq: no
Buildrequires: gettext
Requires: php >= 5.1.0
Requires: httpd >= 2.2.0
Requires: php-xml
Requires: php-imap
Requires: php-mbstring
Requires: php-mcrypt
Requires: php-gd
Requires: php-mcrypt
Requires: php-imap
Requires: php-tidy
Requires: php-mbstring
Requires: php-pecl(Fileinfo)
Requires: php-pecl(memcache)
Requires: php-pear(DB)
Requires: php-pear(File)
Requires: php-pear(Log)
Requires: php-pear(Mail_Mime)
Requires: php-pear(Auth_SASL)
Requires: php-pear(Date)
Requires: php-pear(HTTP_Request)
Requires: php-pear(Mail)
Requires: php-pear(Net_Socket)
Requires: php-pear(Net_SMTP)
Requires: php-pear(Net_Sieve)

%description

Horde Groupware Webmail Edition is a free, enterprise ready, browser based communication suite. Users can read, send and organize email messages and manage and share calendars, contacts, tasks and notes with the standards compliant components from the Horde Project. Horde Groupware Webmail Edition bundles the separately available applications IMP, Ingo, Kronolith, Turba, Nag and Mnemo.

http://www.horde.org/

This build for Centos5

http://www.centos.org/


%prep

%setup -q -n %{name}-%{version}

%build

%install

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -dm 755 $RPM_BUILD_ROOT%{contentdir}/webmail
cp -pR * $RPM_BUILD_ROOT%{contentdir}/webmail

install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d

%clean 
rm -fr $RPM_BUILD_ROOT

%post

echo "Database not set. Install php-mysql if you want to use Mysql"

%preun

%files
%defattr(-,root,root)
# Apache webmail.conf file 
%config(noreplace) %{_sysconfdir}/httpd/conf.d/webmail.conf
# Include top level with %dir so not all files are sucked in
%dir %{contentdir}/webmail
# Include top-level files by hand
%{contentdir}/webmail/*.php
# Include these dirs so that all files _will_ get sucked in
# For Horde Framework
%{contentdir}/webmail/lib
%{contentdir}/webmail/locale
%{contentdir}/webmail/po
%{contentdir}/webmail/scripts
%{contentdir}/webmail/templates
%{contentdir}/webmail/util
%{contentdir}/webmail/admin
%{contentdir}/webmail/js
%{contentdir}/webmail/services
%{contentdir}/webmail/themes
%{contentdir}/webmail/pear
%{contentdir}/webmail/rpc
# Extra files
%{contentdir}/webmail/config/registry.d/README
%{contentdir}/webmail/notconfigured.html
#
# For other Horde Modules
#
%{contentdir}/webmail/imp
%{contentdir}/webmail/dimp
%{contentdir}/webmail/mimp
%{contentdir}/webmail/kronolith
%{contentdir}/webmail/nag
%{contentdir}/webmail/ingo
%{contentdir}/webmail/turba
%{contentdir}/webmail/mnemo
# Mark documentation files with %doc and %docdir
%doc %{contentdir}/webmail/COPYING
%doc %{contentdir}/webmail/README
%docdir %{contentdir}/webmail/docs
%{contentdir}/webmail/docs 
# Mark configuration files with %config and use secure permissions
# (note that .dist files are considered software; don't mark %config)
# For Horde
%attr(750,root,%{apachegroup}) %dir %{contentdir}/webmail/config
%defattr(640,root,%{apachegroup})
%{contentdir}/webmail/config/.htaccess
%{contentdir}/webmail/config/*.dist
%config(noreplace) %{contentdir}/webmail/config/*.php
%config(noreplace) %{contentdir}/webmail/config/*.xml
# For IMP
%attr(750,root,%{apachegroup}) %dir %{contentdir}/webmail/imp/config
%defattr(640,root,%{apachegroup})
%{contentdir}/webmail/imp/config/.htaccess
%{contentdir}/webmail/imp/config/*.dist
%config(noreplace) %{contentdir}/webmail/imp/config/*.php
%config(noreplace) %{contentdir}/webmail/imp/config/*.xml
#
# For DIMP
%attr(750,root,%{apachegroup}) %dir %{contentdir}/webmail/dimp/config
%defattr(640,root,%{apachegroup})
%{contentdir}/webmail/dimp/config/.htaccess
%{contentdir}/webmail/dimp/config/*.dist
%config(noreplace) %{contentdir}/webmail/dimp/config/*.php
%config(noreplace) %{contentdir}/webmail/dimp/config/*.xml
#
# For MIMP
%attr(750,root,%{apachegroup}) %dir %{contentdir}/webmail/mimp/config
%defattr(640,root,%{apachegroup})
%{contentdir}/webmail/mimp/config/.htaccess
%{contentdir}/webmail/mimp/config/*.dist
%config(noreplace) %{contentdir}/webmail/mimp/config/*.php
%config(noreplace) %{contentdir}/webmail/mimp/config/*.xml
#
# For Kronolith
%attr(750,root,%{apachegroup}) %dir %{contentdir}/webmail/kronolith/config
%defattr(640,root,%{apachegroup})
%{contentdir}/webmail/kronolith/config/.htaccess
%{contentdir}/webmail/kronolith/config/*.dist
%config(noreplace) %{contentdir}/webmail/kronolith/config/*.php
%config(noreplace) %{contentdir}/webmail/kronolith/config/*.xml
#
# For NAG
%attr(750,root,%{apachegroup}) %dir %{contentdir}/webmail/nag/config
%defattr(640,root,%{apachegroup})
%{contentdir}/webmail/nag/config/.htaccess
%{contentdir}/webmail/nag/config/*.dist
%config(noreplace) %{contentdir}/webmail/nag/config/*.php
%config(noreplace) %{contentdir}/webmail/nag/config/*.xml
#
# For Ingo
%attr(750,root,%{apachegroup}) %dir %{contentdir}/webmail/ingo/config
%defattr(640,root,%{apachegroup})
%{contentdir}/webmail/ingo/config/.htaccess
%{contentdir}/webmail/ingo/config/*.dist
%config(noreplace) %{contentdir}/webmail/ingo/config/*.php
%config(noreplace) %{contentdir}/webmail/ingo/config/*.xml
#
# For Turba
%attr(750,root,%{apachegroup}) %dir %{contentdir}/webmail/turba/config
%defattr(640,root,%{apachegroup})
%{contentdir}/webmail/turba/config/.htaccess
%{contentdir}/webmail/turba/config/*.dist
%config(noreplace) %{contentdir}/webmail/turba/config/*.php
%config(noreplace) %{contentdir}/webmail/turba/config/*.xml
#
# For mnemo
%attr(750,root,%{apachegroup}) %dir %{contentdir}/webmail/mnemo/config
%defattr(640,root,%{apachegroup})
%{contentdir}/webmail/mnemo/config/.htaccess
%{contentdir}/webmail/mnemo/config/*.dist
%config(noreplace) %{contentdir}/webmail/mnemo/config/*.php
%config(noreplace) %{contentdir}/webmail/mnemo/config/*.xml

# Output from rpmbuild


%changelog
* Thu Feb 05 2009 Norliyana Kamarludin <norliyana@oscc.org.my> 1.2.2
- Fix security issues

* Tue Sep 16 2008 Harisfazillah Jamel <haris@oscc.org.my> 1.1.3
- Added in more configuration for other Horde modules
- SPEC From Horde 3.1.7 RPM SPEC Centos Extras Repos

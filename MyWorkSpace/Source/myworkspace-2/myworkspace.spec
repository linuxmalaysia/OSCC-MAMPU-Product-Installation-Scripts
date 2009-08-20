#%define contentdir /usr/share/
#%define apacheuser apache
#%define apachegroup apache

Summary: MyWorkSpace Email Server Installer By OSCC MAMPU
Name: myworkspace
Version: 2
Release: 1
Source: myworkspace-%{version}.%{release}.tar.bz2
License: LGPL
Group: Applications/Internet
Vendor:   OSCC MAMPU
Packager: Harisfazillah Jamel <haris@oscc.org.my>
URL: http://myworkspace.oscc.org.my/
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
AutoReq: no
Requires: sed
Requires: php >= 4.3.0
Requires: httpd >= 2.0.46
Requires: mysql
Requires: mysql-server
Requires: mysql-devel
Requires: php-mysql
Requires: postfix
Requires: openldap
Requires: php-ldap
Requires: openldap-servers
Requires: openldap-clients
Requires: horde-webmail
Requires: aspell
Requires: dbmail-mysql >= 2.2.10

%description

MyWorkSpace Email Server Installer By OSCC MAMPU. MyWorkSpace will install Postfix, Dbmail, Mysql, Openldap, Horde Groupware Webmail Edition.

OSCC MAMPU
http://www.oscc.org.my/

Horde Framework
http://www.horde.org/

Dbmail
http://www.dbmail.org/

R&D Team
Open Source Competency Centre (OSCC),
Lot E302-E304, Enterprise Building 3,
63000 Cyberjaya, Malaysia.
Tel. 603 83191200, Fax: 603 83193206
Mobile : 019-6085482
email : haris@oscc.org.my linuxmalaysia@gmail.com
http://blog.harisfazillah.info/

# Macro for generating an environment variable (%1) with %2 random characters
# from gforge spec
%define randstr() %1=`perl -e 'for ($i = 0, $bit = "!", $key = ""; $i < %2; $i++) {while ($bit !~ /^[0-9A-Za-z]$/) { $bit = chr(rand(90) + 32); } $key .= $bit; $bit = "!"; } print "$key";'`

%prep

%setup -q -n %{name}-%{version}

%build

%install

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/oscc
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/oscc/myworkspace

cp -pR * $RPM_BUILD_ROOT%{_sysconfdir}/oscc/myworkspace

%clean
rm -fr $RPM_BUILD_ROOT

%post

# Most of the part are done here. Where are using sed fot this.
# http://howto.landure.fr/gnu-linux/debian-4-0-etch-en/install-horde-groupware-webmail-edition-on-debian-4-0-etch

# Setting PHP for Horde. Remember to restart Apache

cp /etc/php.ini /etc/oscc/php.ini.ori

# Set Memory limit for PHP
sed -i -e 's/memory_limit = .*/memory_limit = 500M/' /etc/php.ini
sed -i -e 's/post_max_size = .*/post_max_size = 500M/' /etc/php.ini
sed -i -e 's/upload_max_filesize = .*/upload_max_filesize = 500M/' /etc/php.ini

# Copying Horde config

cp -f /etc/oscc/myworkspace/horde/config/conf.php /usr/share/webmail/config/conf.php

### Loading Default Horde Mysql Database
###

if [ $1 -eq 1 ]; then
    # Initial install.  Create and populate Horde mysql database

    echo "Configuration Start. Please answer all the questions, if any."

    service mysqld status | grep 'is running' >/dev/null 2>&1 || service mysqld start

    mysqladmin create webmail

if [ $? -eq 0 ]; then

    %randstr GFPASS 8

    echo "GRANT ALL ON webmail.* to webmail@localhost identified by '$GFPASS';" > /etc/oscc/webmail-install-$$.tmp
    mysql webmail < /etc/oscc/webmail-install-$$.tmp
    rm /etc/oscc/webmail-install-$$.tmp
    echo "Loading Database Horde"
    mysql webmail < /usr/share/webmail/scripts/sql/groupware.sql


#### Setting in horde conf.php $conf['sql']['password'] = 'password';
sed -i -e "s/^\(.*sql.*password.*=\).*;/\1 '$GFPASS';/" /usr/share/webmail/config/conf.php

#### Setting in horde conf.php $conf['sessionhandler']['params']['password'] = 'password';
sed -i -e "s/^\(.*sessionhandler.*params.*password.*=\).*;/\1 '$GFPASS';/" /usr/share/webmail/config/conf.php

else

echo "*** ERROR*** You horde database is already created or your upgrading your webmail."

fi

echo "Webmail database ready"

fi

### end of loading Horde Database

### Restart all services

echo "start services needed by MyWorkSpace"

service mysqld restart

sleep 10

#service dbmail-lmtpd restart
#service dbmail-pop3d restart
#service dbmail-imapd restart
#service dbmail-timsieved restart

service httpd restart

# Make sure it start after reboot server

chkconfig mysqld on
chkconfig httpd on


%preun

%files
%defattr(-,root,root)
/etc/oscc/myworkspace/horde/config/conf.php
%doc /etc/oscc/myworkspace/README.oscc


# Apache webmail.conf file
#%config(noreplace) %{_sysconfdir}/httpd/conf.d/webmail.conf
# Include top level with %dir so not all files are sucked in
#%dir %{contentdir}/webmail
# Include top-level files by hand
#%{contentdir}/webmail/*.php
# Mark documentation files with %doc and %docdir
#%doc %{contentdir}/webmail/COPYING
#%doc %{contentdir}/webmail/README
#%docdir %{contentdir}/webmail/docs
#%{contentdir}/webmail/docs
# Mark configuration files with %config and use secure permissions
# (note that .dist files are considered software; don't mark %config)
# For Horde
#%attr(750,root,%{apachegroup}) %dir %{contentdir}/webmail/config
#%defattr(640,root,%{apachegroup})
#%{contentdir}/webmail/config/.htaccess
#%{contentdir}/webmail/config/*.dist
#%config(noreplace) %{contentdir}/webmail/config/*.php
#%config(noreplace) %{contentdir}/webmail/config/*.xml

# Output from rpmbuild


%changelog
* Wed Sep 17 2008 Harisfazillah Jamel <haris@oscc.org.my> 2.1
- First Installer


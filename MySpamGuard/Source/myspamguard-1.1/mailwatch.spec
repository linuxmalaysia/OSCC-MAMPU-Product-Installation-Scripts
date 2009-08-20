Summary: Mailwatch Installation Script
Name: mailwatch
Version: 1.0.4
Release: 1
Source0: %{name}-%{version}.tar.gz
#Source0: mailwatch-1.0.4.tar.gz
License: GPL
Vendor:   OSCC MAMPU.
Packager: Maisarah Ishak <maisarah@oscc.org.my> 
Group: System Environment/Daemons
BuildArchitectures: noarch
Requires: wget, php-common, httpd
Requires: php-mysql, mysql, mysql-server
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
Mailwatch Installation script

%prep

%setup -q

#changes to the default MailWatch.pm file:

sed -i -e's/\(^my($db_user)\W*=\)\(.*$\)/\1 'mailwatch'/'	\
	-e's/\(^my($db_pass)\W*=\)\(.*$\)/\1 'oscc123'/' MailWatch.pm
	
#changes to conf.php in mailscanner directory:

sed -i -e's/\(^define(DB_USER\W*,\)\(.*$\)/\1 '\''mailwatch'\'');/' mailscanner/conf.php.example
sed -i -e's/\(^define(DB_PASS\W*,\)\(.*$\)/\1 '\''oscc123'\'');/' mailscanner/conf.php.example
#sed -i -e's,\(^define(MAILWATCH_HOME\W*,\)\(.*$\),\1 /var/www/html/mailscanner,' mailscanner/conf.php.example 
sed -i -e's/\(^define(QUARANTINE_USE_FLAG\W*,\)\(.*$\)/\1 '\''true'\'');/' mailscanner/conf.php.example
sed -i -e's/\(^define(QUARANTINE_MAIL_HOST\W*,\)\(.*$\)/\1 '\''127.0.0.1'\'');/' mailscanner/conf.php.example
sed -i -e's/\(^define(QUARANTINE_FROM_ADDR\W*,\)\(.*$\)/\1 '\''postmaster@oscc.org.my'\'');/' mailscanner/conf.php.example
sed -i -e's/\(^define(MAILQ\W*,\)\(.*$\)/\1 '\''false'\'');/' mailscanner/conf.php.example

%build

%install

rm -rf %{buildroot}

install -d -m 755 %{buildroot}/var/www/html/mailscanner
install -d -m 755 %{buildroot}/var/www/html/mailscanner/cache
install -d -m 755 %{buildroot}/var/www/html/mailscanner/temp
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 755 %{buildroot}%{_libdir}/%{name}
cp -pR *.pm %{buildroot}%{_sysconfdir}/%{name}
cp -pR *.sql %{buildroot}%{_sysconfdir}/%{name}
cp -pR mailscanner/* %{buildroot}/var/www/html/mailscanner
cp %{buildroot}/var/www/html/mailscanner/conf.php.example %{buildroot}/var/www/html/mailscanner/conf.php
#cp %{buildroot}%{_sysconfdir}/%{name}/MailWatch.pm %{buildroot}%{_libdir}/%{name}

%clean

rm -rf %{buildroot}

%post

#load database
if [ $1 -eq 1 ]; then
  #initial install. Create and populate DB.

  echo "Configuration Start. Please answer all the questions"

  service mysqld status | grep 'is running'>/dev/null 2>&1 || service mysqld start
   
  mysql < /etc/mailwatch/create.sql

  echo "GRANT ALL ON mailscanner.* TO mailwatch@localhost IDENTIFIED BY 'oscc123';">/tmp/mailwatch-install-$$.tmp

  mysql mailscanner < /tmp/mailwatch-install-$$.tmp

  #mysql mailscanner -u mailwatch -p oscc123

  echo "INSERT INTO users VALUES ('admin',md5('oscc123'),'admin','A','0','0','0','0','0');">/tmp/mailwatch-install2-$$.tmp

  mysql mailscanner < /tmp/mailwatch-install2-$$.tmp

  #mysql > INSERT INTO users VALUES ('admin',md5('oscc123'),'admin','A','0','0','0','0','0');

fi

#change permission of /var/www/html/mailscanner

chown apache:apache /var/www/html/mailscanner/images
chmod ug+rwx /var/www/html/mailscanner/images
chown apache:apache /var/www/html/mailscanner/cache
chmod ug+rwx /var/www/html/mailscanner/cache
chown apache /var/www/html/mailscanner/temp
chmod g+w /var/www/html/mailscanner/temp

#copy conf.php.example and rename it as conf.php
#cp %{buildroot}/var/www/html/mailscanner/conf.php.example %{buildroot}/var/www/html/mailscanner/conf.php

# Send the information
#wget http://www.oscc.org.my/myspamguard.html

%files
%defattr(-,root,root)
%doc CHANGELOG LICENSE INSTALL USER_FILTERS UPGRADING
%doc tools luser 
%doc fix_quarantine_permissions mailq.php create.sql
%config(noreplace) %{_sysconfdir}/%{name}
/var/www/html/mailscanner

%preun

%changelog
* Wed Aug 1 2007 Maisarah Ishak <maisarah@oscc.org.my>
- Generate mailwatch.spec for OSCC

* Fri Jun 22 2007 Hisham Mohd Aderis <hisham@oscc.org.my>
- insert command to install oscc.repo to user's machine pointing to repos.oscc.org.my(0.0.2)

* Fri May 18 2007 Harisfazillah Jamel <haris@oscc.org.my>
- alpha 0.0.1 this include Linux counter script counter.li.org

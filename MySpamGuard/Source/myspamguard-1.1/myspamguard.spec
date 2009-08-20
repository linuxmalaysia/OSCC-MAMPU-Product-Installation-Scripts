Summary: MySpamGuard Installation Script
Name: myspamguard 
Version: 1.1
Release: 1
Source0: %{name}-%{version}.tar.gz
License: GPL
Vendor:   OSCC MAMPU.
Packager: Maisarah Ishak <maisarah@oscc.org.my> 
Group: System Environment/Daemons
BuildArchitectures: noarch
Requires: wget
Requires: spamassassin
#Requires: mailwatch 
Requires: postfix
Requires: httpd 
Requires: mysql, mysql-server 
Requires: php, php-mysql, php-gd, zlib 
Requires: perl-DBI, perl-DBD-MySql, perl-Convert-BinHex, perl-IO-stringy, perl-TimeDate, perl-Net-CIDR, perl-MailTools, perl-MIME-tools, perl-HTML-Parser, perl-Convert-TNEF, perl-Filesys-Df, perl-Sys-Hostname-Long, perl-DBD-SQLite, sqlite, tnef 
Requires: clamav, clamd 


BuildRoot: %{_tmppath}/%{name}-%{version}

%description
MySpamGuard Installation script

%prep

%setup -q
	
%build

%clean 
rm -rf %{buildroot} 

%install
rm -rf %{buildroot}


%post

#rpm -Uvh --nodeps /usr/src/redhat/RPMS/noarch/mailscanner-4.61.6-1.noarch.rpm
#rpm -Uvh /usr/src/redhat/RPMS/noarch/mailwatch-1.0.4-1.noarch.rpm

#cp %{_sysconfdir}/mailwatch/MailWatch.pm %{buildroot}%{_libdir}/MailScanner/MailScanner/CustomFunctions/

# Send the information
#wget http://www.oscc.org.my/myspamguard.html

%files
%defattr(-,root,root)

%preun

%changelog
* Fri Aug 3 2007 Maisarah Ishak <maisarah@oscc.org.my>
- Generate myspamguard.spec for OSCC

* Fri Jun 22 2007 Hisham Mohd Aderis <hisham@oscc.org.my>
- insert command to install oscc.repo to user's machine pointing to repos.oscc.org.my(0.0.2)

* Fri May 18 2007 Harisfazillah Jamel <haris@oscc.org.my>
- alpha 0.0.1 this include Linux counter script counter.li.org

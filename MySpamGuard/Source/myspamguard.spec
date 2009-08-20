#SPEC for MySpamGuard

Summary: MySpamGuard Installation Script
Name: myspamguard 
Version: 1.1
Release: 3.oscc
Source0: %{name}-%{version}.tar.gz
License: GPL
Vendor:   OSCC MAMPU.
Packager: Maisarah Ishak <maisarah@oscc.org.my> 
Group: System Environment/Daemons
BuildArchitectures: noarch
Requires: wget
Requires: spamassassin
Requires: mailwatch 
Requires: postfix
Requires: httpd 
Requires: mysql, mysql-server 
Requires: php, php-mysql, php-gd, zlib 
Requires: perl-DBI, perl-DBD-MySQL, perl-Convert-BinHex, perl-IO-stringy, perl-TimeDate, perl-Net-CIDR, perl-MailTools, perl-MIME-tools, perl-HTML-Parser, perl-Convert-TNEF, perl-Filesys-Df, perl-Sys-Hostname-Long, perl-DBD-SQLite, sqlite, tnef 
Requires: perl-Net-IP, perl-Archive-Zip, perl-Compress-Zlib, perl-HTML-Tagset
Requires: clamav, clamav-db, clamd 
Requires: mailscanner, MailScanner-perl-MIME-Base64
#Requires: oscc-repos, oscc-tracking
Requires: oscc-bayesian 


BuildRoot: %{_tmppath}/%{name}-%{version}

%description
MySpamGuard Installation script

%prep

%setup 

	
%build

%clean 
rm -rf %{buildroot} 

%install
rm -rf %{buildroot}

%post


#changing /etc/MailScanner/MailScanner.conf
sed -i -e's/\(^Run As User\W*=\)\(\W*$\)/\1 postfix/'   \
        -e's/\(^Run As Group\W*=\)\(\W*$\)/\1 postfix/' \
        -e's,\(^Incoming Queue Dir\W*=\)\(.*$\),\1 /var/spool/postfix/hold,'    \
        -e's,\(^Outgoing Queue Dir\W*=\)\(.*$\),\1 /var/spool/postfix/incoming,'        \
        -e's/\(^MTA\W*=\)\(.*$\)/\1 postfix/'   \
        -e's/\(^Always Looked Up Last\W*=\)\(.*$\)/\1 \&MailWatchLogging/'      \
        -e's/\(^Detailed Spam Report\W*=\)\(.*$\)/\1 yes/'      \
        -e's/\(^Quarantine Whole Message\W*=\)\(.*$\)/\1 yes/'  \
        -e's/\(^Quarantine Whole Message As Queue Files\W*=\)\(.*$\)/\1 no/'    \
        -e's/\(^Include Scores In SpamAssassin Report\W*=\)\(.*$\)/\1 yes/'     \
        -e's/\(^Quarantine User\W*=\)\(.*$\)/\1 apache/'        \
        -e's/\(^Quarantine Group\W*=\)\(.*$\)/\1 apache/'       \
        -e's/\(^Quarantine Permissions\W*=\)\(.*$\)/\1 0660/'   \
        -e's/\(^Spam Actions\W*=\)\(.*$\)/\1 store/'    \
        -e's/\(^High Scoring Spam Actions\W*=\)\(.*$\)/\1 store/'    \
        -e's/\(^Spam List\W*=\)\(.*$\)/\1 spamhaus-ZEN NJABL spamcop.net/'    \
        -e's/\(^Use SpamAssassin\W*=\)\(.*$\)/\1 yes/'  \
        -e's/\(^Log Spam\W*=\)\(.*$\)/\1 yes/'  \
        -e's,\(^SpamAssassin User State Dir\W*=\)\(.*$\),\1 /var/spool/MailScanner/spamassassin,'       \
	-e's,\(^Clam Socket\W*=\)\(.*$\),\1 /tmp/clamd.socket,'    \
        -e's,\(^Clam Lock File\W*=\)\(.*$\),\1 /var/lock/subsys/clamd,'    \
        -e's/\(^Send Notices\W*=\)\(.*$\)/\1 no/'      \
        -e's/\(^Log Speed\W*=\)\(.*$\)/\1 yes/'      \
        -e's/\(^Virus Scanners\W*=\)\(.*$\)/\1 clamav/' /etc/MailScanner/MailScanner.conf

#changing /var/spool/MailScanner/incoming
chown postfix.postfix /var/spool/MailScanner/incoming

#changing /var/spool/MailScanner/quarantine
chown postfix.postfix /var/spool/MailScanner/quarantine

cp %{_sysconfdir}/mailwatch/MailWatch.pm %{_libdir}/MailScanner/MailScanner/CustomFunctions/

#Configure postfix via postconf
postconf -e "header_checks = regexp:/etc/postfix/header_checks"
echo "/^Received:/ HOLD" >> /etc/postfix/header_checks

#changing /etc/postfix/main.cf
sed -i -e's/\(^inet_interfaces\W*=\)\(.*$\)/\1 all/' /etc/postfix/main.cf


#stop SendMail
service sendmail stop
chkconfig sendmail off

#start MailScanner and add it to the list of services
service MailScanner start
chkconfig --add MailScanner
chkconfig MailScanner on

#restart apache services
service httpd restart

# Send the information
NAMASERVER=`uname -n`
wget -nc http://repos.oscc.org.my/myspamguard-$NAMASERVER.html

#start clamd services
service clamd start
chkconfig --add clamd
chkconfig clamd on

# Update clamav and spamassassin

echo "Updating Clamav"
freshclam

echo "Updating SA Rules"
sa-update

%files
%defattr(-,root,root)

%preun

#stop MailScanner and delete from list of services
service MailScanner stop
chkconfig MailScanner off



%changelog
* Wed Nov 19 2008 Norliyana Kamarludin <norliyana@oscc.org.my>
- rebuild for repos2

* Tue May 20 2008 Jamalulkhair <jamal@oscc.org.my>
- replace ORDBL with NJABL

* Fri Aug 24 2007 Maisarah Ishak <maisarah@oscc.org.my>
-update 2nd release of mySpamGuard
-change config in Mailscanner.conf

* Tue Aug 7 2007 Maisarah Ishak <maisarah@oscc.org.my>
- Generate myspamguard.spec for OSCC

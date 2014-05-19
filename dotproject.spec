%define svn_snap r6063
%define __noautoreq /usr/bin/php

Summary:	Web Based Project Management Tool
Name:		dotproject
Version:	2.1.4
Release:	0.0.%{svn_snap}.5
License:	GPL
Group:		System/Servers
URL:		http://sourceforge.net/projects/dotproject/
Source0:	http://prdownloads.sourceforge.net/dotproject/%{name}-%{version}-%{svn_snap}.tar.xz
# S10 - S30 was taken http://sourceforge.net/projects/dotmods/
Source10:	http://mesh.dl.sourceforge.net/project/dotmods/Annotations/0.3.0/annotations_1235-29072009.zip
Source11:	http://mesh.dl.sourceforge.net/project/dotmods/Backup%20Module/v2.0/backup_2.0.tar.gz
Source12:	http://mesh.dl.sourceforge.net/project/dotmods/Details/0.3.0/details_1235-29072009.zip
Source13:	http://mesh.dl.sourceforge.net/project/dotmods/Eventum%20Integration%20Module/v1.1.5/dp_eventum_1_1_5.zip
Source14:	http://mesh.dl.sourceforge.net/project/dotmods/Finance/finance%200.1/finance.zip
# cvs -z3 -d:pserver:anonymous@dotmods.cvs.sourceforge.net:/cvsroot/dotmods co -P helpdesk
Source15:	helpdesk.tar.gz
Source16:	http://mesh.dl.sourceforge.net/project/dotmods/Holiday/Version%201.2/holiday_v1_2.tar.gz
Source17:	http://mesh.dl.sourceforge.net/project/dotmods/Import%20Export/backup%200.2/backup.zip
# cvs -z3 -d:pserver:anonymous@dotmods.cvs.sourceforge.net:/cvsroot/dotmods co -P inventory
Source18:	inventory.tar.gz
Source19:	http://mesh.dl.sourceforge.net/project/dotmods/Invoice/invoice_0.7.tar.gz
Source20:	http://mesh.dl.sourceforge.net/project/dotmods/Journal%20Module/v1.0a/journal.zip
Source21:	http://mesh.dl.sourceforge.net/project/dotmods/Opportunities/0.3.0/opportunities_1235-29072009.zip
Source22:	http://mesh.dl.sourceforge.net/project/dotmods/ProjectDesigner/ProjectDesigner%20v1/projectdesigner_v1.zip
# cvs -z3 -d:pserver:anonymous@dotmods.cvs.sourceforge.net:/cvsroot/dotmods co -P risks
Source23:	risks.tar.gz
Source24:	http://mesh.dl.sourceforge.net/project/dotmods/Trac%20Integration/Release%200.5/trac_dotmod-0.5.1.tar.gz
Source25:	http://mesh.dl.sourceforge.net/project/dotmods/Unitcost/v1.0.0/unitcost_1.0.0.tar.gz
Patch0:		dotproject-2.1.2-fix-perl-path.patch
Patch1:		dotproject-external_smarty.diff
Patch2:		dotproject-external_nusoap.diff
Patch3:		dotproject-external_adodb.diff
Requires(post): rpm-helper apache-mod_php
Requires(preun): rpm-helper apache-mod_php
Requires:	apache-mod_php
Requires:	apache-mod_socache_shmcb
Requires:	nusoap
Requires:	php-adodb
Requires:	php-gd
Requires:	php-jpgraph
Requires:	php-ldap
Requires:	php-mysql
Requires:	php-pear-Date_Holidays
Requires:	php-smarty
Requires:	php-sqlite3
BuildArch:	noarch
BuildRequires:	apache-devel >= 2.0.54
BuildRequires:	unzip

%description
DotProject is a Web-based project management framework that includes modules
for companies, projects, tasks (with Gantt charts), forums, files, a
calendar, contacts, tickets/helpdesk, multi-language support, user/module
permissions, and themes. It is translated into 17 languages and has a modular
design that allows extra modules (such as time sheets and inventory) to be
added in easily.

%prep
%setup -q

# extra modules
pushd modules

if ! [ -d annotations ]; then unzip -q %{SOURCE10}; else exit 1; fi
if ! [ -d backup ]; then tar -zxf %{SOURCE11}; else exit 1; fi
if ! [ -d details ]; then unzip -q %{SOURCE12}; else exit 1; fi
if ! [ -d eventum ]; then unzip -q %{SOURCE13}; else exit 1; fi
if ! [ -d finance ]; then unzip -q %{SOURCE14}; else exit 1; fi
if ! [ -d helpdesk ]; then tar -zxf %{SOURCE15}; else exit 1; fi
if ! [ -d holiday ]; then tar -zxf %{SOURCE16}; else exit 1; fi

# special voodoo magic here...
if ! [ -d import_export ]; then
    mkdir -p import_export
    pushd import_export
	unzip -q %{SOURCE17}
	mv backup/* .
	rm -rf backup
	perl -pi -e "s|\'Backup\'\;|\'Import_Export\'\;|g" setup.php
	perl -pi -e "s|\'backup\'\;|\'import_export\'\;|g" setup.php
    popd
else
    exit 1
fi

if ! [ -d inventory ]; then tar -zxf %{SOURCE18}; else exit 1; fi
if ! [ -d invoice ]; then tar -zxf %{SOURCE19}; else exit 1; fi

# more special voodoo magic here.
if ! [ -d journal ]; then
    cd ..
    unzip -q %{SOURCE20}
    cd -
else
    exit 1
fi

if ! [ -d opportunities ]; then unzip -q %{SOURCE21}; else exit 1; fi
if ! [ -d projectdesigner ]; then unzip -q %{SOURCE22}; else exit 1; fi
if ! [ -d risks ]; then tar -zxf %{SOURCE23}; else exit 1; fi
if ! [ -d trac ]; then tar -zxf %{SOURCE24}; else exit 1; fi
if ! [ -d unitcost ]; then tar -zxf %{SOURCE25}; else exit 1; fi

popd

# don't bundle these
#rm -rf lib/PEAR
rm -rf lib/adodb
rm -rf lib/jpgraph
rm -rf lib/smarty
rm -f lib/phpgacl/soap/nusoap.php
rm -rf modules/holiday/PEAR

%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

# fix dir/file perms
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# clean up SVN stuff
for i in `find . -type d -name .svn` `find . -type f -name .svn\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# unwanted files
find . -type f -name "Thumbs.db" -exec rm -f {} \;

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%install
export DONT_RELINK=1

install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_datadir}/%{name}

cp -aRf * %{buildroot}%{_datadir}/%{name}/

install -d %{buildroot}%{_datadir}/%{name}/files/cache/phpgacl
install -d %{buildroot}%{_datadir}/%{name}/files/cache/smarty_templates
install -d %{buildroot}%{_datadir}/%{name}/files/cache/smarty_templates_c

# fix file perms
chmod 755 %{buildroot}%{_datadir}/%{name}/includes/gateway.pl
cp %{buildroot}%{_datadir}/%{name}/includes/gateway.pl %{buildroot}%{_datadir}/%{name}/modules/helpdesk/gateway.pl

# fix config file location
cp %{buildroot}%{_datadir}/%{name}/includes/config-dist.php %{buildroot}%{_sysconfdir}/%{name}/config.php
ln -s %{_sysconfdir}/%{name}/config.php %{buildroot}%{_datadir}/%{name}/includes/config.php

cat > dotproject-apache.conf << EOF

Alias /%{name} "%{_datadir}/%{name}"

<Directory "%{_datadir}/%{name}">
    Require all granted
    php_admin_value memory_limit    64M
    php_admin_value post_max_size   17M
    php_admin_value upload_max_filesize 32M
    php_admin_value max_execution_time 120
</Directory>

<Directory "%{_datadir}/%{name}/files">
    Options -All
    Require all denied
</Directory>

<Directory "%{_datadir}/%{name}/files/temp">
    Options -All
    Require all granted
</Directory>

<Directory "%{_datadir}/%{name}/includes">
    <Files "gateway.pl">
	Require all denied
    </Files>
</Directory>

<Directory "%{_datadir}/%{name}/install">
    Require host 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf"
</Directory>
EOF

install -m0644 dotproject-apache.conf %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf

# cleanup
find %{buildroot}%{_datadir}/%{name} -type f -name "\.htaccess" | xargs rm -f


%files
%doc ChangeLog
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%attr(0640,apache,apache) %config(noreplace) %{_sysconfdir}/%{name}/config.php
%{_datadir}/%{name}

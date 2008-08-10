%define snap r794

#Module-Specific definitions
%define mod_name mod_auth_ntlm_winbind
%define mod_conf B19_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Enables the Apache Web Server to Authenticate Users against Microsoft like DCs
Name:		apache-%{mod_name}
Version:	0.0.0
Release:	%mkrel 0.%{snap}.4
Group:		System/Servers
License:	Apache License
URL:		http://adldap.sourceforge.net/wiki/doku.php?id=mod_auth_ntlm_winbind
Source0:	%{mod_name}-%{version}-%{snap}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache-mpm-prefork >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_auth_ntlm_winbind is an Apache module to authenticate users and
authorize access through Samba's winbind daemon against a Microsoft
like Domain Controller (DC).  These are Microsoft NT/2000/XP and Samba.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} %{mod_conf}

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type d -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -DAPACHE2 -c %{mod_name}.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

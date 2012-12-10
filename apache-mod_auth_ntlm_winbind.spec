%define snap r794

#Module-Specific definitions
%define mod_name mod_auth_ntlm_winbind
%define mod_conf B19_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Enables the Apache Web Server to Authenticate Users against Microsoft like DCs
Name:		apache-%{mod_name}
Version:	0.0.0
Release:	0.%{snap}.10
Group:		System/Servers
License:	Apache License
URL:		http://adldap.sourceforge.net/wiki/doku.php?id=mod_auth_ntlm_winbind
Source0:	%{mod_name}-%{version}-%{snap}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_auth_ntlm_winbind-20060510-connect_http10.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache-mpm-prefork >= 2.2.0
Requires:	samba-common
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file

%description
mod_auth_ntlm_winbind is an Apache module to authenticate users and
authorize access through Samba's winbind daemon against a Microsoft
like Domain Controller (DC).  These are Microsoft NT/2000/XP and Samba.

%prep

%setup -q -n %{mod_name}
%patch0 -p0

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

%{_bindir}/apxs -DAPACHE2 -c %{mod_name}.c

%install

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

%files
%doc AUTHORS README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r794.10mdv2012.0
+ Revision: 772569
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r794.9
+ Revision: 678265
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r794.8mdv2011.0
+ Revision: 587923
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r794.7mdv2010.1
+ Revision: 516049
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r794.6mdv2010.0
+ Revision: 406539
- rebuild

* Sun Mar 22 2009 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r794.5mdv2009.1
+ Revision: 360275
- fix deps
- add the proxy patch (rediffed from contrib/)

* Sun Aug 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r794.4mdv2009.0
+ Revision: 270221
- fix url

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r794.3mdv2009.0
+ Revision: 234662
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r794.2mdv2009.0
+ Revision: 215534
- fix rebuild

* Sat May 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r794.1mdv2009.0
+ Revision: 205372
- new svn snap (r794)

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r781.2mdv2008.1
+ Revision: 181672
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 29 2007 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r781.1mdv2008.1
+ Revision: 93833
- import apache-mod_auth_ntlm_winbind


* Sat Sep 29 2007 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-0.r781.1mdv2008.0
- initial Mandriva package

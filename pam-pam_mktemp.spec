%define 	modulename pam_mktemp
Summary:	Pluggable private /tmp space support for interactive (shell) sessions.
Summary(pl):	Modu³ PAM zarz±dzaj±cy prywatn± przestrzeni± tymczasowych plików u¿ytkownika
Name:		pam-%{modulename}
Version:	0.2.5
Release:	0.1
License:	relaxed BSD and (L)GPL-compatible
Group:		Applications/System
URL:		http://www.openwall.com/pam/
Source0:	ftp://ftp.openwall.com/pub/projects/pam/modules/%{modulename}/%{modulename}-%version.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PAM module which may be used with a PAM-aware login
service to provide per-user private directories under /tmp as a part
of PAM session or account management.

%description -l pl
Modu³ PAM zapewniaj±cy podczas logowania prywatny podkatalog /tmp dla
plików tymczasowych danego u¿ytkownika w ramach zarz±dzania sesj± lub
kontem przez PAM.

%prep
%setup -q -n %{modulename}-%{version}

%build
%{__make} CFLAGS="-Wall -fPIC -DLINUX_PAM %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
mkdir -p -m 711 /tmp/.private

%triggerin -- e2fsprogs
if [ -d /tmp/.private -a -O /tmp/.private ]; then
	chattr +a /tmp/.private 2> /dev/null || :
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README
/lib/security/pam_mktemp.so

%define 	modulename pam_mktemp
Summary:	Pluggable private /tmp space support for interactive (shell) sessions.
Summary(pl.UTF-8):	Moduł PAM zarządzający prywatną przestrzenią tymczasowych plików użytkownika
Name:		pam-%{modulename}
Version:	1.0.3
Release:	0.1
License:	relaxed BSD and (L)GPL-compatible
Group:		Applications/System
Source0:	ftp://ftp.openwall.com/pub/projects/pam/modules/%{modulename}/%{modulename}-%{version}.tar.gz
# Source0-md5:	0276521b0ce91de356e70a4b82030c0d
Patch0:		%{name}-include.patch
URL:		http://www.openwall.com/pam/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PAM module which may be used with a PAM-aware login service to provide
per-user private directories under /tmp as a part of PAM session or
account management.

%description -l pl.UTF-8
Moduł PAM zapewniający podczas logowania prywatny podkatalog /tmp dla
plików tymczasowych danego użytkownika w ramach zarządzania sesją lub
kontem przez PAM.

%prep
%setup -q -n %{modulename}-%{version}
%patch0 

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="-Wall -fPIC -DLINUX_PAM %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%attr(755,root,root) /%{_lib}/security/pam_mktemp.so

#
# Conditional build:
%bcond_without	static_libs	# static libraries
#

%define		gitref	fa54a467

Summary:	A Comprehensive Open Source Library for Galois Field Arithmetic
Name:		gf-complete
Version:	1.03
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://git.sr.ht/~thestr4ng3r/gf-complete/archive/%{gitref}.tar.gz#/%{name}-%{version}.tar.gz
# Source0-md5:	365f844eda38d2e369341bdfbbf05565
Patch0:		opt.patch
URL:		https://web.eecs.utk.edu/~jplank/plank/www/software.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Comprehensive Open Source Library for Galois Field Arithmetic.

%package tools
Summary:	Galois Field Arithmetic calculations tools
Summary(pl.UTF-8):	Wspólne pliki biblioteki %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description tools
Galois Field Arithmetic calculations tools.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q -n %{name}-%{gitref}
%patch -P 0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%ifarch %{ix86}
	--disable-sse \
	--disable-avx \
%endif
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc License.txt README
%attr(755,root,root) %{_libdir}/libgf_complete.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgf_complete.so.1

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gf_add
%attr(755,root,root) %{_bindir}/gf_div
%attr(755,root,root) %{_bindir}/gf_inline_time
%attr(755,root,root) %{_bindir}/gf_methods
%attr(755,root,root) %{_bindir}/gf_mult
%attr(755,root,root) %{_bindir}/gf_poly
%attr(755,root,root) %{_bindir}/gf_time

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgf_complete.so
%{_libdir}/libgf_complete.la
%{_includedir}/gf_*.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgf_complete.a
%endif

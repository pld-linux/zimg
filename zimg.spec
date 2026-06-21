# NOTE: for http://zimg.buaa.us/ see zimg-storage.spec
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Z img - resizing, colorspace and bit depth conversion library
Summary(pl.UTF-8):	Z img - biblioteka do zmiany rozmiaru oraz przekształceń przestrzeni i głębi barw
Name:		zimg
Version:	3.0.6
Release:	1
License:	WTFPL v2 (library)
Group:		Libraries
#Source0Download: https://github.com/sekrit-twc/zimg/releases
Source0:	https://github.com/sekrit-twc/zimg/archive/release-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b2184ea83017b0026235af1dd0e54388
URL:		https://github.com/sekrit-twc/zimg
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The "z" library implements the commonly required image processing
basics of scaling, colorspace conversion, and depth conversion. A
simple API enables conversion between any supported formats to operate
with minimal knowledge from the programmer. All library routines were
designed from the ground-up with flexibility, thread-safety, and
correctness as first priorities. Allocation, buffering, and I/O are
cleanly separated from processing, allowing the programmer to adapt
"z" to many scenarios.

%description -l pl.UTF-8
Biblioteka "z" implementuje często wymagane podstawowe operacje
przetwarzania obrazu, takie jak skalowanie oraz przekształcenia
przestrzeni i głębi barw. Proste API pozwala na konwersję między
dowolnymi obsługiwanymi formatami, wymagając od programisty minimum
wiedzy. Wszystkie funkcje biblioteki zostały zaprojektowane z myślą o
elastyczności, bezpiecznym użyciu współbieżnym oraz poprawnością.
Przydzielanie pamięci, buforowanie oraz operacje we/wy są odizolowane
od przetwarzania, co pozwala programiście adaptować bibliotekę "z" do
wielu scenariuszy.

%package devel
Summary:	Header files for Z img library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Z img
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for Z img library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Z img.

%package static
Summary:	Static Z img library
Summary(pl.UTF-8):	Statyczna biblioteka Z img
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Z img library.

%description static -l pl.UTF-8
Statyczna biblioteka Z img.

%prep
%setup -q -n zimg-release-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libzimg.la

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/zimg/example $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/zimg

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README.md
%{_libdir}/libzimg.so.*.*.*
%ghost %{_libdir}/libzimg.so.2

%files devel
%defattr(644,root,root,755)
%{_libdir}/libzimg.so
%{_includedir}/zimg.h
%{_includedir}/zimg++.hpp
%{_pkgconfigdir}/zimg.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libzimg.a
%endif

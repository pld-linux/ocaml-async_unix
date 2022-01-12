#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Monadic concurrency library
Summary(pl.UTF-8):	Biblioteka współbieżności monadowej
Name:		ocaml-async_unix
Version:	0.14.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/janestreet/async_unix/tags
Source0:	https://github.com/janestreet/async_unix/archive/v%{version}/async_unix-%{version}.tar.gz
# Source0-md5:	fe550f16eb858adaa970d88ecf7ba858
URL:		https://github.com/janestreet/async_unix
BuildRequires:	ocaml >= 1:4.08.0
BuildRequires:	ocaml-async_kernel-devel >= 0.14
BuildRequires:	ocaml-async_kernel-devel < 0.15
BuildRequires:	ocaml-core-devel >= 0.14
BuildRequires:	ocaml-core-devel < 0.15
BuildRequires:	ocaml-core_kernel-devel >= 0.14
BuildRequires:	ocaml-core_kernel-devel < 0.15
BuildRequires:	ocaml-dune >= 2.0.0
BuildRequires:	ocaml-ppx_jane-devel >= 0.14
BuildRequires:	ocaml-ppx_jane-devel < 0.15
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Async_unix includes Unix-related dependencies for things like system
calls and threads. Using these, it hooks the Async_kernel scheduler up
to either epoll or select, depending on availability, and manages a
thread pool that blocking system calls run in.

This package contains files needed to run bytecode executables using
async_unix library.

%description -l pl.UTF-8
Async_unix zawiera związane z Uniksem zależności dla elementów takich
jak wywołania systemowe czy wątki. Przy ich użyciu podpina planistę
Async_kernel do wywołań epoll lub select, w zależności od dostępności,
i zarządza pulą wątków, w której działają blokujące wywołania
systemowe.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki async_unix.

%package devel
Summary:	Monadic concurrency library - development part
Summary(pl.UTF-8):	Biblioteka współbieżności monadowej - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml
Requires:	ocaml-async_kernel-devel >= 0.14
Requires:	ocaml-core-devel >= 0.14
Requires:	ocaml-core_kernel-devel >= 0.14
Requires:	ocaml-ppx_jane-devel >= 0.14

%description devel
This package contains files needed to develop OCaml programs using
async_unix library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki async_unix.

%prep
%setup -q -n async_unix-%{version}

%build
dune build --release --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/async_unix/*.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/async_unix/*/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/async_unix

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.md
%dir %{_libdir}/ocaml/async_unix
%{_libdir}/ocaml/async_unix/META
%{_libdir}/ocaml/async_unix/*.cma
%dir %{_libdir}/ocaml/async_unix/thread_pool
%{_libdir}/ocaml/async_unix/thread_pool/*.cma
%dir %{_libdir}/ocaml/async_unix/thread_safe_ivar
%{_libdir}/ocaml/async_unix/thread_safe_ivar/*.cma
%dir %{_libdir}/ocaml/async_unix/thread_safe_pipe
%{_libdir}/ocaml/async_unix/thread_safe_pipe/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/async_unix/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/async_unix/thread_pool/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/async_unix/thread_safe_ivar/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/async_unix/thread_safe_pipe/*.cmxs
%endif
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllasync_unix_stubs.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/async_unix/libasync_unix_stubs.a
%{_libdir}/ocaml/async_unix/*.cmi
%{_libdir}/ocaml/async_unix/*.cmt
%{_libdir}/ocaml/async_unix/*.cmti
%{_libdir}/ocaml/async_unix/*.mli
%{_libdir}/ocaml/async_unix/thread_pool/*.cmi
%{_libdir}/ocaml/async_unix/thread_pool/*.cmt
%{_libdir}/ocaml/async_unix/thread_pool/*.cmti
%{_libdir}/ocaml/async_unix/thread_pool/*.mli
%{_libdir}/ocaml/async_unix/thread_safe_ivar/*.cmi
%{_libdir}/ocaml/async_unix/thread_safe_ivar/*.cmt
%{_libdir}/ocaml/async_unix/thread_safe_ivar/*.cmti
%{_libdir}/ocaml/async_unix/thread_safe_ivar/*.mli
%{_libdir}/ocaml/async_unix/thread_safe_pipe/*.cmi
%{_libdir}/ocaml/async_unix/thread_safe_pipe/*.cmt
%{_libdir}/ocaml/async_unix/thread_safe_pipe/*.cmti
%{_libdir}/ocaml/async_unix/thread_safe_pipe/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/async_unix/async_unix.a
%{_libdir}/ocaml/async_unix/*.cmx
%{_libdir}/ocaml/async_unix/*.cmxa
%{_libdir}/ocaml/async_unix/thread_pool/thread_pool.a
%{_libdir}/ocaml/async_unix/thread_pool/*.cmx
%{_libdir}/ocaml/async_unix/thread_pool/*.cmxa
%{_libdir}/ocaml/async_unix/thread_safe_ivar/thread_safe_ivar.a
%{_libdir}/ocaml/async_unix/thread_safe_ivar/*.cmx
%{_libdir}/ocaml/async_unix/thread_safe_ivar/*.cmxa
%{_libdir}/ocaml/async_unix/thread_safe_pipe/thread_safe_pipe.a
%{_libdir}/ocaml/async_unix/thread_safe_pipe/*.cmx
%{_libdir}/ocaml/async_unix/thread_safe_pipe/*.cmxa
%endif
%{_libdir}/ocaml/async_unix/dune-package
%{_libdir}/ocaml/async_unix/opam

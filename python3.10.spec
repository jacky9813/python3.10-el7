
%global pybasever 3.10
%global pyshortver 310
%global pyfullver %{pybasever}.13

%global pip_version 23.0.1
%global setuptools_version 65.5.0

Name:           python%{pybasever}
Version:        %{pyfullver}
Release:        1%{?dist}.jackychen
License:        Python-2.0.1
Summary:        A non-official build of Python %{pybasever} interpreter
URL:            https://www.python.org/
Source0:        %{url}ftp/python/%{pyfullver}/Python-%{pyfullver}.tgz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bluez-libs-devel
BuildRequires:  bzip2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  expat-devel
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gdb
BuildRequires:  gdbm-devel
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  gmp-devel
BuildRequires:  gnupg
BuildRequires:  libffi-devel
BuildRequires:  libuuid-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  openssl11-devel
BuildRequires:  perl-core
BuildRequires:  pkgconfig
BuildRequires:  readline-devel
BuildRequires:  sqlite-devel
BuildRequires:  tar
BuildRequires:  tcl-devel
BuildRequires:  tix-devel
BuildRequires:  tk-devel
BuildRequires:  tzdata
BuildRequires:  xz-devel
BuildRequires:  zlib-devel


%global pylibdir %{_libdir}/python%{pybasever}
%global dynload_dir %{pylibdir}/lib-dynload
%global bytecode_suffixes .cpython-%{pyshortver}*.pyc

%global _pyconfig_h pyconfig-%{__isa_bits}.h

%global platform_triplet %{expand:%(echo %{_arch}-linux%{_gnu} | sed -E \\
    -e 's/^arm(eb)?-linux-gnueabi$/arm\\1-linux-gnueabihf/' \\
    -e 's/^mips64(el)?-linux-gnu$/mips64\\1-linux-gnuabi64/' \\
    -e 's/^ppc(64)?(le)?-linux-gnu$/powerpc\\1\\2-linux-gnu/')}

%global ABIFLAGS %{nil}

%global LDVERSION %{pybasever}%{ABIFLAGS}

%global SOABI cpython-%{pyshortver}%{ABIFLAGS}-%{platform_triplet}

%global py_SOVERSION 1.0
%global py_INSTSONAME libpython%{LDVERSION}.so.%{py_SOVERSION}

###################################
# Provides section
###################################
# Base Python
Provides:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       python%{pyshortver} = %{version}-%{release}
Obsoletes:      python%{pyshortver} < %{version}-%{release}

# Pip
Provides:       bundled(python%{pybasever}dist(pip)) = %{pip_version}
Provides:       %{name}-pip = %{pip_version}
Conflicts:      %{name}-pip < %{pip_version}

# Setuptools
Provides:       bundled(python%{pybasever}dist(setuptools)) = %{setuptools_version}
Provides:       %{name}-setuptools = %{setuptools_version}

# 2to3
Provides:       %{name}-2to3 = %{version}-%{release}

# Idle
Provides:       %{name}-idle = %{version}-%{release}
Provides:       %{name}-tools = %{version}-%{release}
Provides:       %{name}-tools%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-tools < %{version}-%{release}

# module tkinter
Provides:       %{name}-tkinter = %{version}-%{release}
Provides:       %{name}-turtle = %{version}-%{release}

%global __requires_exclude ^/usr/bin/python3.10|libpython3.10.*$

%description
Python %{pybasever} is an accessible, high-level, dynamically typed, interpreted
programming language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

This is an non-official Python %{pybasever} by Jacky Chen. Check 
https://github.com/jacky9813/python3.10-el7 for RPM Spec source code.

%prep
%setup -q -n Python-%{pyfullver}

find -name '*.exe' -print -delete

rm -r Modules/expat

rm configure pyconfig.h.in

%build
export HAS_GIT=not-found

autoconf
autoheader

# Here I specified --disable-test-modules to reduce installed package size, as
# user wouldn't need test scripts for testing Python build.
# These files, however, is compiled in official Python build and packaged into
# package like python3-test.

%configure \
    --enable-ipv6 \
    --enable-shared \
    --disable-test-modules \
    --with-platlibdir=%{_lib} \
    --with-system-expat \
    --with-system-ffi \
    --without-static-libpython \
    --enable-loadable-sqlite-extensions

%make_build

%install

# Use altinstall.
%{__make} altinstall DESTDIR=%{?buildroot}

[ -f %{buildroot}%{_bindir}/python3 ] && rm %{buildroot}%{_bindir}/python3
[ -f %{buildroot}%{_bindir}/pydoc3 ] && rm %{buildroot}%{_bindir}/pydoc3
[ -f %{buildroot}%{_bindir}/pip3 ] && rm %{buildroot}%{_bindir}/pip3
[ -f %{buildroot}%{_bindir}/idle3 ] && rm %{buildroot}%{_bindir}/idle3
[ -f %{buildroot}%{_bindir}/2to3 ] && rm %{buildroot}%{_bindir}/2to3
[ -f %{buildroot}%{_libdir}/libpython3.so ] && rm %{buildroot}%{_libdir}/libpython3.so
[ -f %{buildroot}%{_mandir}/man1/python3.1 ] && rm %{buildroot}%{_mandir}/man1/python3.1
[ -f %{buildroot}%{_libdir}/pkgconfig/python3.pc ] && rm %{buildroot}%{_libdir}/pkgconfig/python3.pc
[ -f %{buildroot}%{_libdir}/pkgconfig/python3-embed.pc ] && rm %{buildroot}%{_libdir}/pkgconfig/python3-embed.pc
ls %{buildroot}%{_bindir}/python3-* > /dev/null && rm %{buildroot}%{_bindir}/python3-* || true


# As the file said, vendor may patch the shebang in cgi.py.
sed -i "s|#! */usr/local/bin/python|#! %{_bindir}/python%{pybasever}|" %{buildroot}%{_libdir}/python%{pybasever}/cgi.py

# For some reason, the shebang of installed pip points to /usr/bin/python instead
# of /usr/bin/python3.10. The script below is to change that.

sed -i "s|%{_bindir}/python|%{_bindir}/python%{pybasever}|" %{buildroot}%{_bindir}/pip%{pybasever}

%files
####################################################################
# Files that should belongs to python%{pybasever}
####################################################################

%doc README.rst
%{_bindir}/python%{pybasever}
%{_bindir}/pydoc%{pybasever}
%{_bindir}/python%{pybasever}-config

####################################################################
# Files that should belongs to python%{pybasever}-libs
####################################################################

%{_libdir}/%{py_INSTSONAME}
%{_libdir}/libpython%{LDVERSION}.so

%dir %{pylibdir}

%license %{pylibdir}/LICENSE.txt

%dir %{pylibdir}/unittest/
%dir %{pylibdir}/unittest/__pycache__/
%{pylibdir}/unittest/*.py
%{pylibdir}/unittest/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/asyncio/
%dir %{pylibdir}/asyncio/__pycache__/
%{pylibdir}/asyncio/*.py
%{pylibdir}/asyncio/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/venv/
%dir %{pylibdir}/venv/__pycache__/
%{pylibdir}/venv/*.py
%{pylibdir}/venv/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/venv/scripts

%{pylibdir}/wsgiref
%{pylibdir}/xmlrpc

%dir %{pylibdir}/ensurepip/
%dir %{pylibdir}/ensurepip/__pycache__/
%{pylibdir}/ensurepip/*.py
%{pylibdir}/ensurepip/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/ensurepip/_bundled
%{pylibdir}/ensurepip/_bundled/pip-%{pip_version}-py3-none-any.whl
%{pylibdir}/ensurepip/_bundled/setuptools-%{setuptools_version}-py3-none-any.whl
%{pylibdir}/ensurepip/_bundled/__init__.py
%{pylibdir}/ensurepip/_bundled/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/concurrent/
%dir %{pylibdir}/concurrent/__pycache__/
%{pylibdir}/concurrent/*.py
%{pylibdir}/concurrent/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/concurrent/futures/
%dir %{pylibdir}/concurrent/futures/__pycache__/
%{pylibdir}/concurrent/futures/*.py
%{pylibdir}/concurrent/futures/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/pydoc_data

%{dynload_dir}/_blake2.%{SOABI}.so
%{dynload_dir}/_md5.%{SOABI}.so
%{dynload_dir}/_sha1.%{SOABI}.so
%{dynload_dir}/_sha256.%{SOABI}.so
%{dynload_dir}/_sha3.%{SOABI}.so
%{dynload_dir}/_sha512.%{SOABI}.so

%{dynload_dir}/_asyncio.%{SOABI}.so
%{dynload_dir}/_bisect.%{SOABI}.so
%{dynload_dir}/_bz2.%{SOABI}.so
%{dynload_dir}/_codecs_cn.%{SOABI}.so
%{dynload_dir}/_codecs_hk.%{SOABI}.so
%{dynload_dir}/_codecs_iso2022.%{SOABI}.so
%{dynload_dir}/_codecs_jp.%{SOABI}.so
%{dynload_dir}/_codecs_kr.%{SOABI}.so
%{dynload_dir}/_codecs_tw.%{SOABI}.so
%{dynload_dir}/_contextvars.%{SOABI}.so
%{dynload_dir}/_crypt.%{SOABI}.so
%{dynload_dir}/_csv.%{SOABI}.so
%{dynload_dir}/_ctypes.%{SOABI}.so
%{dynload_dir}/_curses.%{SOABI}.so
%{dynload_dir}/_curses_panel.%{SOABI}.so
%{dynload_dir}/_decimal.%{SOABI}.so
%{dynload_dir}/_dbm.%{SOABI}.so
%{dynload_dir}/_elementtree.%{SOABI}.so
%{dynload_dir}/_gdbm.%{SOABI}.so
%{dynload_dir}/_hashlib.%{SOABI}.so
%{dynload_dir}/_heapq.%{SOABI}.so
%{dynload_dir}/_json.%{SOABI}.so
%{dynload_dir}/_lsprof.%{SOABI}.so
%{dynload_dir}/_lzma.%{SOABI}.so
%{dynload_dir}/_multibytecodec.%{SOABI}.so
%{dynload_dir}/_multiprocessing.%{SOABI}.so
%{dynload_dir}/_opcode.%{SOABI}.so
%{dynload_dir}/_pickle.%{SOABI}.so
%{dynload_dir}/_posixsubprocess.%{SOABI}.so
%{dynload_dir}/_queue.%{SOABI}.so
%{dynload_dir}/_random.%{SOABI}.so
%{dynload_dir}/_socket.%{SOABI}.so
%{dynload_dir}/_sqlite3.%{SOABI}.so
%{dynload_dir}/_ssl.%{SOABI}.so
%{dynload_dir}/_statistics.%{SOABI}.so
%{dynload_dir}/_struct.%{SOABI}.so
%{dynload_dir}/array.%{SOABI}.so
%{dynload_dir}/audioop.%{SOABI}.so
%{dynload_dir}/binascii.%{SOABI}.so
%{dynload_dir}/cmath.%{SOABI}.so
%{dynload_dir}/_datetime.%{SOABI}.so
%{dynload_dir}/fcntl.%{SOABI}.so
%{dynload_dir}/grp.%{SOABI}.so
%{dynload_dir}/math.%{SOABI}.so
%{dynload_dir}/mmap.%{SOABI}.so
%{dynload_dir}/nis.%{SOABI}.so
%{dynload_dir}/ossaudiodev.%{SOABI}.so
%{dynload_dir}/_posixshmem.%{SOABI}.so
%{dynload_dir}/pyexpat.%{SOABI}.so
%{dynload_dir}/readline.%{SOABI}.so
%{dynload_dir}/resource.%{SOABI}.so
%{dynload_dir}/select.%{SOABI}.so
%{dynload_dir}/spwd.%{SOABI}.so
%{dynload_dir}/syslog.%{SOABI}.so
%{dynload_dir}/termios.%{SOABI}.so
%{dynload_dir}/unicodedata.%{SOABI}.so
%{dynload_dir}/_uuid.%{SOABI}.so
%{dynload_dir}/xxlimited.%{SOABI}.so
%{dynload_dir}/xxlimited_35.%{SOABI}.so
%{dynload_dir}/_xxsubinterpreters.%{SOABI}.so
%{dynload_dir}/zlib.%{SOABI}.so
%{dynload_dir}/_zoneinfo.%{SOABI}.so

%dir %{pylibdir}/site-packages/
%{pylibdir}/site-packages/README.txt

%{pylibdir}/*.py
%dir %{pylibdir}/__pycache__/
%{pylibdir}/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/collections/
%dir %{pylibdir}/collections/__pycache__/
%{pylibdir}/collections/*.py
%{pylibdir}/collections/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/ctypes/
%dir %{pylibdir}/ctypes/__pycache__/
%{pylibdir}/ctypes/*.py
%{pylibdir}/ctypes/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/ctypes/macholib

%{pylibdir}/curses

%dir %{pylibdir}/dbm/
%dir %{pylibdir}/dbm/__pycache__/
%{pylibdir}/dbm/*.py
%{pylibdir}/dbm/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/distutils/
%dir %{pylibdir}/distutils/__pycache__/
%{pylibdir}/distutils/*.py
%{pylibdir}/distutils/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/distutils/README
%{pylibdir}/distutils/command

%dir %{pylibdir}/email/
%dir %{pylibdir}/email/__pycache__/
%{pylibdir}/email/*.py
%{pylibdir}/email/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/email/mime
%doc %{pylibdir}/email/architecture.rst

%{pylibdir}/encodings

%{pylibdir}/html
%{pylibdir}/http

%dir %{pylibdir}/importlib/
%dir %{pylibdir}/importlib/__pycache__/
%{pylibdir}/importlib/*.py
%{pylibdir}/importlib/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/importlib/metadata/
%dir %{pylibdir}/importlib/metadata/__pycache__/
%{pylibdir}/importlib/metadata/*.py
%{pylibdir}/importlib/metadata/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/json/
%dir %{pylibdir}/json/__pycache__/
%{pylibdir}/json/*.py
%{pylibdir}/json/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/logging
%{pylibdir}/multiprocessing

%dir %{pylibdir}/sqlite3/
%dir %{pylibdir}/sqlite3/__pycache__/
%{pylibdir}/sqlite3/*.py
%{pylibdir}/sqlite3/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/urllib
%{pylibdir}/xml
%{pylibdir}/zoneinfo

%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages
%endif


####################################################################
# Files that should belongs to python%{pybasever}-2to3
####################################################################

%{_bindir}/2to3-%{pybasever}
%{pylibdir}/lib2to3

####################################################################
# Files that should belongs to python%{pybasever}-idle
####################################################################

%{_bindir}/idle%{pybasever}
%{pylibdir}/idlelib

####################################################################
# Files that should belongs to python%{pybasever}-tkinter
####################################################################

%{dynload_dir}/_tkinter.%{SOABI}.so

%{pylibdir}/tkinter

# %{pylibdir}/turtle.py
# %{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}

%{pylibdir}/turtledemo


####################################################################
# Files that should belongs to python%{pybasever}-doc
####################################################################

%{_mandir}/man1/python3.10.1.gz


####################################################################
# Files that should belongs to python%{pybasever}-devel
####################################################################
%{_libdir}/pkgconfig/python-%{LDVERSION}.pc
%{_libdir}/pkgconfig/python-%{LDVERSION}-embed.pc

# Build config
%dir %{pylibdir}/config-%{pybasever}-%{platform_triplet}
%{pylibdir}/config-%{pybasever}-%{platform_triplet}/*

# Includes
%dir %{_includedir}/python3.10
%dir %{_includedir}/python3.10/internal
%dir %{_includedir}/python3.10/cpython
%{_includedir}/python3.10/*.h
%{_includedir}/python3.10/internal/*.h
%{_includedir}/python3.10/cpython/*.h


####################################################################
# Files that should belongs to python%{pybasever}-pip
####################################################################
%{_bindir}/pip%{pybasever}

%{_prefix}/lib/python%{pybasever}/site-packages/pip-%{pip_version}.dist-info
%{_prefix}/lib/python%{pybasever}/site-packages/pip

####################################################################
# Files that should belongs to
# * python%{pybasever}-setuptools
# * python%{pybasever}-pkg_resources
####################################################################

%{_prefix}/lib/python%{pybasever}/site-packages/distutils-precedence.pth
%{_prefix}/lib/python%{pybasever}/site-packages/_distutils_hack

%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools-%{setuptools_version}.dist-info
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools

%changelog

* Tue Sep 19 2023 Jacky Chen <jacky9813@hotmail.com> - 3.10.13-1.jackychen
- Initial Python 3.10 package.


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
BuildRequires:  mpdecimal-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl11-devel
BuildRequires:  perl-core
BuildRequires:  pkgconfig
BuildRequires:  readline-devel
BuildRequires:  sqlite-devel
BuildRequires:  tar
BuildRequires:  tcl-devel
BuildRequires:  tix-devel
BuildRequires:  tzdata
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

Provides:       python%{pybasever} = %{version}-%{release}
Provides:       python%{pybasever}
Provides:       python%{pyshortver} = %{version}-%{release}
Obsoletes:      python%{pyshortver} < %{version}-%{release}

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

%description
Python %{pybasever} is an accessible, high-level, dynamically typed, interpreted
programming language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

%prep
%setup -q -n Python-%{pyfullver}
# %gpgverify -k2 -s1 -d0

find -name '*.exe' -print -delete

rm -r Modules/expat

rm configure pyconfig.h.in

%build
export HAS_GIT=not-found

autoconf
autoheader

topdir=$(pwd)

# export CFLAGS="$(pkg-config --cflags openssl11)"
# export LDFLAGS="$(pkg-config --libs openssl11)"
# export DFLAGS=" "

%configure \
    --enable-ipv6 \
    --enable-shared \
    --disable-test-modules \
    --with-platlibdir=%{_lib} \
    --with-system-expat \
    --with-system-ffi \
    --without-static-libpython \
    --enable-loadable-sqlite-extensions \

%make_build

%install

%make_install

rm %{buildroot}%{_bindir}/python3
rm %{buildroot}%{_bindir}/pydoc3
rm %{buildroot}%{_bindir}/pip3
rm %{buildroot}%{_bindir}/idle3
rm %{buildroot}%{_bindir}/python3-*
rm %{buildroot}%{_bindir}/2to3
rm %{buildroot}%{_libdir}/libpython3.so
rm %{buildroot}%{_mandir}/man1/python3.1
rm %{buildroot}%{_libdir}/pkgconfig/python3.pc
rm %{buildroot}%{_libdir}/pkgconfig/python3-embed.pc

%files
%doc README.rst
%{_bindir}/python%{pybasever}
%{_bindir}/2to3-%{pybasever}
%{_bindir}/pip%{pybasever}
%{_bindir}/idle%{pybasever}
%{_bindir}/pydoc%{pybasever}
%{_bindir}/python%{pybasever}-config
%{_libdir}/%{py_INSTSONAME}

%dir %{pylibdir}

%license %{pylibdir}/LICENSE.txt

%{pylibdir}/lib2to3
# %exclude %{pylibdir}/lib2to3/tests

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

# %{pylibdir}/turtle.py
# %{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}

%dir %{pylibdir}/idlelib
%dir %{pylibdir}/idlelib/Icons
%dir %{pylibdir}/idlelib/__pycache__
%{pylibdir}/idlelib/*.txt
%{pylibdir}/idlelib/*.py
%{pylibdir}/idlelib/*.def
%{pylibdir}/idlelib/ChangeLog
%{pylibdir}/idlelib/help.html
%{pylibdir}/idlelib/idle.bat
%{pylibdir}/idlelib/idle.pyw
%{pylibdir}/idlelib/Icons/README.txt
%{pylibdir}/idlelib/Icons/*.ico
%{pylibdir}/idlelib/Icons/*.png
%{pylibdir}/idlelib/Icons/*.gif
%{pylibdir}/idlelib/__pycache__/*%{bytecode_suffixes}


%dir %{pylibdir}/tkinter
%dir %{pylibdir}/tkinter/__pycache__
%{pylibdir}/tkinter/*.py
%{pylibdir}/tkinter/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/turtledemo
%dir %{pylibdir}/turtledemo/__pycache__
%{pylibdir}/turtledemo/*.py
%{pylibdir}/turtledemo/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/turtledemo/turtle.cfg

%exclude %{_mandir}/man1/python3.10.1.gz

%{pylibdir}/urllib
%{pylibdir}/xml
%{pylibdir}/zoneinfo

%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages
%endif

%{_libdir}/libpython%{LDVERSION}.so
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

# site-packages
%dir %{_prefix}/lib/python%{pybasever}/site-packages/_distutils_hack
%dir %{_prefix}/lib/python%{pybasever}/site-packages/_distutils_hack/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip-23.0.1.dist-info
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/cli
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/cli/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/commands
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/commands/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/distributions
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/distributions/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/index
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/index/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/locations
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/locations/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/metadata
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/metadata/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/metadata/importlib
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/metadata/importlib/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/models
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/models/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/network
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/network/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/build
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/build/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/install
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/install/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/req
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/req/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/legacy
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/legacy/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/resolvelib
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/resolvelib/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/utils
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/utils/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/vcs
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/vcs/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/cachecontrol
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/cachecontrol/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/cachecontrol/caches
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/cachecontrol/caches/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/certifi
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/certifi/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/cli
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/cli/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/metadata
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/metadata/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/colorama
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/colorama/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/colorama/tests
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/colorama/tests/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/distlib
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/distlib/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/distro
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/distro/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/idna
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/idna/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/msgpack
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/msgpack/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/packaging
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/packaging/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pkg_resources
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pkg_resources/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/platformdirs
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/platformdirs/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/filters
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/filters/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/formatters
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/formatters/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/lexers
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/lexers/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/styles
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/styles/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyparsing
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyparsing/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyparsing/diagram
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyparsing/diagram/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyproject_hooks
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyproject_hooks/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyproject_hooks/_in_process
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyproject_hooks/_in_process/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/requests
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/requests/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/resolvelib
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/resolvelib/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/resolvelib/compat
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/resolvelib/compat/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/rich
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/rich/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/tenacity
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/tenacity/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/tomli
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/tomli/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/contrib
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/contrib/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/contrib/_securetransport
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/packages
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/packages/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/packages/backports
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/packages/backports/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/util
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/util/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/webencodings
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/webencodings/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/importlib_resources
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/importlib_resources/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/jaraco
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/jaraco/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/jaraco/text
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/jaraco/text/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/more_itertools
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/more_itertools/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/packaging
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/packaging/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/pyparsing
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/pyparsing/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/pyparsing/diagram
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/pyparsing/diagram/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/extern
%dir %{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/extern/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools-65.5.0.dist-info
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_distutils
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_distutils/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_distutils/command
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_distutils/command/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/importlib_metadata
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/importlib_metadata/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/importlib_resources
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/importlib_resources/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/jaraco
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/jaraco/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/jaraco/text
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/jaraco/text/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/more_itertools
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/more_itertools/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/packaging
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/packaging/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/pyparsing
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/pyparsing/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/pyparsing/diagram
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/pyparsing/diagram/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/tomli
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/tomli/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/command
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/command/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/config
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/config/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/config/_validate_pyproject
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/config/_validate_pyproject/__pycache__
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/extern
%dir %{_prefix}/lib/python%{pybasever}/site-packages/setuptools/extern/__pycache__

%{_prefix}/lib/python%{pybasever}/site-packages/setuptools-65.5.0.dist-info/*
%{_prefix}/lib/python%{pybasever}/site-packages/pip-23.0.1.dist-info/*
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/*.exe
"%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/command/launcher manifest.xml"
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/*.tmpl
%{_prefix}/lib/python%{pybasever}/site-packages/pip/py.typed
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/vendor.txt
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/distlib/*.exe
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/certifi/cacert.pem
%{_prefix}/lib/python%{pybasever}/site-packages/distutils-precedence.pth

%{_prefix}/lib/python%{pybasever}/site-packages/_distutils_hack/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/cli/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/commands/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/distributions/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/index/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/locations/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/metadata/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/metadata/importlib/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/models/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/network/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/build/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/install/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/req/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/legacy/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/resolvelib/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/utils/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/vcs/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/cachecontrol/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/cachecontrol/caches/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/certifi/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/cli/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/metadata/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/colorama/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/colorama/tests/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/distlib/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/distro/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/idna/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/msgpack/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/packaging/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pkg_resources/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/platformdirs/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/filters/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/formatters/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/lexers/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/styles/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyparsing/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyparsing/diagram/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyproject_hooks/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyproject_hooks/_in_process/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/requests/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/resolvelib/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/resolvelib/compat/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/rich/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/tenacity/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/tomli/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/contrib/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/contrib/_securetransport/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/packages/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/packages/backports/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/util/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/webencodings/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/importlib_resources/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/jaraco/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/jaraco/text/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/more_itertools/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/packaging/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/pyparsing/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/pyparsing/diagram/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/extern/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_distutils/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_distutils/command/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/importlib_metadata/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/importlib_resources/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/jaraco/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/jaraco/text/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/more_itertools/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/packaging/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/pyparsing/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/pyparsing/diagram/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/tomli/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/command/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/config/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/config/_validate_pyproject/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/extern/*.py
%{_prefix}/lib/python%{pybasever}/site-packages/_distutils_hack/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/cli/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/commands/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/distributions/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/index/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/locations/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/metadata/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/metadata/importlib/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/models/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/network/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/build/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/operations/install/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/req/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/legacy/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/resolution/resolvelib/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/utils/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_internal/vcs/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/cachecontrol/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/cachecontrol/caches/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/certifi/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/cli/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/chardet/metadata/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/colorama/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/colorama/tests/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/distlib/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/distro/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/idna/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/msgpack/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/packaging/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pkg_resources/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/platformdirs/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/filters/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/formatters/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/lexers/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pygments/styles/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyparsing/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyparsing/diagram/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyproject_hooks/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/pyproject_hooks/_in_process/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/requests/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/resolvelib/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/resolvelib/compat/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/rich/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/tenacity/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/tomli/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/contrib/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/packages/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/packages/backports/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/urllib3/util/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pip/_vendor/webencodings/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/importlib_resources/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/jaraco/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/jaraco/text/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/more_itertools/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/packaging/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/pyparsing/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/_vendor/pyparsing/diagram/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/pkg_resources/extern/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_distutils/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_distutils/command/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/importlib_metadata/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/importlib_resources/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/jaraco/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/jaraco/text/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/more_itertools/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/packaging/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/pyparsing/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/pyparsing/diagram/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/_vendor/tomli/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/command/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/config/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/config/_validate_pyproject/__pycache__/*%{bytecode_suffixes}
%{_prefix}/lib/python%{pybasever}/site-packages/setuptools/extern/__pycache__/*%{bytecode_suffixes}


%changelog

* Tue Sep 19 2023 Jacky Chen <jacky9813@hotmail.com> - 3.10.13-1
- Initial Python 3.10 package.

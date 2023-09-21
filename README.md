# Python 3.10 RPM package for Enterprise Linux 7

Note: The RPM spec is still in development.

While Fedora Project has [rpms/python3.10](https://src.fedoraproject.org/rpms/python3.10)
RPM source code, it doesn't work on EL7 as it uses multiple new directives that EL7 RPM
cannot support.

## Limitations

* ~~`tkinter` module is not available due to Python 3.10 requires Tk 8.6, while EL7 got
  only Tk 8.5.~~ <br>Although not officially supported, it seems that Python can be
  compiled with Tk 8.5, . This is completed by following the guidance from
  [CPython 3.11 Misc/rhel7](https://github.com/python/cpython/tree/v3.11.5/Misc/rhel7).
    * That being said, I'm not sure what will happen if there's any Tk 8.6 only code
      being used by any Python script. User may have very degraded experience.
* `_ssl` requires `openssl11-libs` from epel repo, I'm not sure whether to put
  `epel-release` as one of the requirement packages or not.
* Unlike official Python build, this package uses builtin `libmpdec` instead of official
  EL7 one, as `libmpdec` Python 3.10 requires 2.5.0 or later while EL7 provides only
  2.4.2 in EPEL repo.
* I'm not planned to unbundle things like python3.10-pip and python3.10-setuptools into
  separated packages. It'll create too much hassle for me when all I want is to get 
  Python working only. (Contribution are welcomed.)
* The built RPM package will not create links for Idle in desktop.
  * I mean c'mon, you should have something like VSCode or PyCharm already, right?

## Build (With Docker, Recommended)

```bash
#!/bin/bash
docker build -t python-rpm:3.10.13-1.el7.jackychen.$(uname -m) .
[ -d build ] && rm -r build
mkdir -p build
docker save python-rpm:3.10.13-1.el7.jackychen.$(uname -m) -o build/3.10.13-1.el7.jackychen.$(uname -m).tar
tar xvf build/3.10.13-1.el7.jackychen.$(uname -m).tar -C build
pushd $(find build/* -type d)
tar xvf layer.tar -C ../
popd
find build/* -type f -not -name '*.rpm' -exec rm {} \;
find build/* -type d | xargs -n 1 rm -r
```

## Build (On local machine)

```bash
#!/bin/bash
yum install -y epel-release rpmdevtools rpmlint
yum-builddep -y python3.10.spec
rpmdev-setuptree
spectool -g -S -R python3.10.spec

export PKG_CONFIG_PATH=$(pwd)/el7-pkgconfig
rpmbuild -bs python3.10.spec
rpmbuild -bb python3.10.spec

# The built RPM packages will exist in ~/rpmbuild/RPMS for binary RPMs and
# ~/rpmbuild/SRPMS for source RPM.
```

## Install RPM

```bash
#!/bin/bash
yum install -y epel-release
yum install -y ./python3.10-3.10.13-1.el7.jackychen.x86_64.rpm
```

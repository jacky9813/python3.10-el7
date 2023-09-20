# Python 3.10 RPM package for Enterprise Linux 7

Note: The RPM spec is still in development.

## Limitations

* `tkinter` module is not available due to Python 3.10 requires Tk 8.6, while EL7 got
  only Tk 8.5.
* `_ssl` requires `openssl11-libs` from epel repo, I'm not sure whether to put
  `epel-release` as one of the requirement packages or not.

## Build (With Docker, Recommended)

```bash
#!/bin/bash
mkdir -p build
docker build -t python-rpm:3.10.13-1.el7.jackychen.$(uname -m) .
docker save python-rpm:3.10.13-1.el7.jackychen.$(uname -m) -o build/3.10.13-1.el7.jackychen.$(uname -m).tar
tar xvf build/3.10.13-1.el7.jackychen.$(uname -m).tar -C build
pushd $(find build/* -type d)
tar xvf layer.tar -C ../
popd
find build/* -type f -not -name '*.rpm' -exec rm {} \;
find build/* -type d | xargs -n 1 rm -r
```

## Build (On local machine)

Caution: This process will temporary replace `/usr/lib64/pkgconfig/openssl.pc` with
`/usr/lib64/pkgconfig/openssl11.pc`.

If not sure what this means, build RPM inside an EL7-based container instead.

```bash
#!/bin/bash
yum install -y epel-release rpmdevtools rpmlint
yum-builddep -y python3.10.spec
HAS_SYSTEM_OPENSSL=
if [ -f /usr/lib64/pkgconfig/openssl.pc ]; then
    if [ -f /usr/lib64/pkgconfig/openssl.pc.backup ]; then
        echo "Unable to backup /usr/lib64/pkgconfig/openssl.pc, aborting"
        exit 1
    fi
    HAS_SYSTEM_OPENSSL=1
    cp /usr/lib64/pkgconfig/openssl.pc /usr/lib64/pkgconfig/openssl.pc.backup
fi

rpmdev-setuptree
spectool -g -S -R python3.10.spec
rpmbuild -bs python3.10.spec
ln -s /usr/lib64/pkgconfig/openssl11.pc /usr/lib64/pkgconfig/openssl.pc
rpmbuild -bb python3.10.spec
rm /usr/lib64/pkgconfig/openssl.pc
if ! [ -z "$HAS_SYSTEM_OPENSSL" ]; then
    rm /usr/lib64/pkgconfig/openssl.pc
    cp /usr/lib64/pkgconfig/openssl.pc.backup /usr/lib64/pkgconfig/openssl.pc
    rm /usr/lib64/pkgconfig/openssl.pc.backup
fi
```

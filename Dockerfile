ARG PYFULLVER=3.10.13

FROM centos:7 as rpm_builder

RUN yum install -y epel-release rpmdevtools rpmlint && \
    rpmdev-setuptree
WORKDIR /root/rpmbuild

FROM rpm_builder as python_builder
ARG PYFULLVER
COPY build-deps SPECS/
ADD https://www.python.org/ftp/python/${PYFULLVER}/Python-${PYFULLVER}.tgz SOURCES/

RUN yum install -y $(cat SPECS/build-deps) && \
    ln -s /usr/lib64/pkgconfig/openssl11.pc /usr/lib64/pkgconfig/openssl.pc

COPY ./python3.10.spec SPECS/

RUN rpmbuild -bs SPECS/python3.10.spec && \
    rpmbuild --noclean -bb SPECS/python3.10.spec

FROM scratch

COPY --from=python_builder /root/rpmbuild/RPMS/*/*.rpm /root/rpmbuild/SRPMS/*.rpm /


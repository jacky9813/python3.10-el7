ARG PYFULLVER=3.10.13

FROM centos:7 as rpm_builder

RUN yum install -y epel-release rpmdevtools rpmlint && \
    rpmdev-setuptree

WORKDIR /root/rpmbuild

ARG PYFULLVER
COPY build-deps SPECS/
ADD https://www.python.org/ftp/python/${PYFULLVER}/Python-${PYFULLVER}.tgz SOURCES/

RUN yum install -y $(cat SPECS/build-deps)


FROM rpm_builder as python_builder

COPY ./python3.10.spec SPECS/
COPY ./el7-pkgconfig /el7-pkgconfig

ENV PKG_CONFIG_PATH /el7-pkgconfig

RUN rpmbuild -bs SPECS/python3.10.spec && \
    rpmbuild --noclean -bb SPECS/python3.10.spec

FROM scratch

COPY --from=python_builder /root/rpmbuild/RPMS/*/*.rpm /root/rpmbuild/SRPMS/*.rpm /


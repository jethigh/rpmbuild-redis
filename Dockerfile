FROM quay.io/centos/centos:stream8 as rpmbuilder8
LABEL org.opencontainers.image.authors="jethigh@protonmail.com"

RUN dnf install -y epel-release epel-next-release && dnf install -y rpmdevtools rpmlint mock git gcc openssl-devel systemd-devel make && dnf clean all && rm -rf /var/cache/dnf

FROM quay.io/centos/centos:centos7 as rpmbuilder7
LABEL org.opencontainers.image.authors="jethigh@protonmail.com"

RUN yum install -y epel-release epel-next-release && yum install -y rpmdevtools rpmlint mock git gcc openssl-devel systemd-devel make && yum clean all && rm -rf /var/cache/yum
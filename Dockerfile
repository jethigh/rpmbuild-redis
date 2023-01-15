FROM quay.io/centos/centos:stream8
LABEL org.opencontainers.image.authors="jethigh@protonmail.com"

RUN dnf install -y epel-release epel-next-release && dnf install -y rpmdevtools rpmlint mock git gcc openssl-devel systemd-devel && dnf clean all && rm -rf /var/cache/dnf
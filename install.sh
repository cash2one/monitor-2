#!/bin/sh

echo "nameserver 8.8.8.8" >> /etc/resolv.conf

yum -y install lrzsz.x86_64

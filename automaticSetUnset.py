#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 Rafael Sene

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

    Contributors:
        * Rafael Sene <rpsene@gmail.com>

    This script was initially created on May 30, 2015. It automatically sets
    all the iptables rules which activates the port-forwarding through the host
    for accessing virtual machines which has a private IP.
"""

import sys
import os


def setFirstRule(ip, port):
    print ("iptables -t nat -A PREROUTING -p tcp --dport %s -j DNAT --to %s:22"\% (port, ip))
    os.system("iptables -t nat -A PREROUTING -p tcp --dport %s -j DNAT --to %s:22" % (port, ip))


def setSecondRule(ip):
    print ("iptables -I FORWARD -d %s/24 -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT" % ip)
    os.system("iptables -I FORWARD -d %s/24 -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT" % ip)


def unsetFirstRule(ip, port):
    print ("iptables -t nat -D PREROUTING -p tcp --dport %s -j DNAT --to %s:22" % (port, ip))
    os.system("iptables -t nat -D PREROUTING -p tcp --dport %s -j DNAT --to %s:22" % (port, ip))


def unsetSecondRule(ip):
    print ("iptables -D FORWARD -d %s/24 -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT" % ip)
    os.system("iptables -D FORWARD -d %s/24 -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT" % ip)


def readIpPortFile(filelocation):
    with open(filelocation) as f:
        lines = f.readlines()
    return lines


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'Usage: python automaticSetUnset.py [action] file'
        print 'action: set or unset'
        exit(1)
    elif os.path.isfile(sys.argv[2]) is False:
        print sys.argv[2] + ' is not a valid file'
        exit(1)
    else:
        if sys.argv[1] == 'set':
            for l in readIpPortFile(sys.argv[2]):
                IP = l.rstrip('\n').split()[0]
                PORT = l.rstrip('\n').split()[1]
                setFirstRule(IP, PORT)
                setSecondRule(IP)
        elif sys.argv[1] == 'unset':
            for l in readIpPortFile(sys.argv[2]):
                IP = l.rstrip('\n').split()[0]
                PORT = l.rstrip('\n').split()[1]
                unsetFirstRule(IP, PORT)
                unsetSecondRule(IP)
        else:
            print 'action: set or unset'
            exit(1)

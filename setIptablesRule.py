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

    This script was initially created on May 30, 2015. It sets a iptables
    rule which activates the port-forwarding through the host for accessing
    virtual machines which has a private IP.
"""

import sys
import os


def setFirstRule(ip, port):
    print ("iptables -t nat -A PREROUTING -p tcp --dport %s -j DNAT --to %s:22" % (port, ip))
    os.system("iptables -t nat -A PREROUTING -p tcp --dport %s -j DNAT --to %s:22" % (port, ip))


def setSecondRule(ip):
    print ("iptables -I FORWARD -d %s/24 -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT" % ip)
    os.system("iptables -I FORWARD -d %s/24 -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT" % ip)


def addToFile(ip, port, filename):
    print ("echo \"%s    %s\" >> %s" % (ip, port, filename))
    os.system("echo \"%s    %s\" >> %s" % (ip, port, filename))


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'Usage: python setIptablesRule.py [Guest IP] [Port]'
    else:
        IP = sys.argv[1]
        PORT = sys.argv[2]
        setFirstRule(IP, PORT)
        setSecondRule(IP)
        addToFile(IP, PORT, './active_ips')

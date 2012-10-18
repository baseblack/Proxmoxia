#!/usr/bin/env python
#######################################
#
# Example: Check cluster logs
#
#######################################

import re
import os
import sys
import time

libpath = os.path.join(os.path.abspath( os.path.dirname(__file__)) , '..')
sys.path.append(libpath)

import proxmox

# connect to one of the proxmox nodes and get authenticated
c = proxmox.Connector('proxmox-7')
c.get_auth_token('root@pam', 'strawberries')

# connect into the cluster to perform actions
p = proxmox.Proxmox(c)

# print cluster logs
for line in p.cluster.log(max=5):
    print "{node}: {user} - {msg}".format(**line)



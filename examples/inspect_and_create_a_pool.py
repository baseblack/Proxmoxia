#!/usr/bin/env python
#######################################
#
# Example: Inspect and create a new pool
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

# create the pool if it doesn't already exist
if 'example_test' not in [x['poolid'] for x in p.pools()]:
    p.pools.post(poolid='example_test', comment="its a god damn pool")

# get information about the pool
print p.pools('example_test')

# and call delete on the pool
p.pools('example_test').delete()


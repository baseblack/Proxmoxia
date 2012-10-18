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

# create a user
if 'andrew.bunday@pve' not in [x['userid'] for x in p.access.users()]:
    p.access.users.post(userid='andrew.bunday@pve', comment="test user", password="strawberries")

print p.access.users()

# get information about the user
print p.access.users('andrew.bunday@pve').get()

## and call delete on the user
p.access.users('andrew.bunday@pve').delete()




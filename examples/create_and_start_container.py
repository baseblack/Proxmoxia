#######################################
#
# Example: Create and start a container
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

# connect to the node you wish to perform actions on.
node = proxmox.Node(c, 'proxmox-7')

# find the path for the template you want to use.
for template in node.storage('virtual-nfs').content(content='vztmpl'):
    if re.match('.*ubuntu-12.04-bb-20121010b_amd64.tar.gz$', template['volid']):
        volume = node.storage('virtual-nfs').content(template['volid']).get()

# create the container, giving it some sensible settings
taskid = node.openvz.post( ostemplate=volume.get('path'),
                           vmid=204,
                           hostname='test-4',
                           ip_address='192.168.123.204',
                           storage='local')

# keep an eye on task and see when its completed
while node.tasks(taskid).status()['status'] == 'running':
        time.sleep(1)

# print out the logs
for line in node.tasks(taskid).log():
    print line['t']

try:
    # start up the container
    node.openvz('204').status.start.post()
except:
    raise Exception('Unable to start container')



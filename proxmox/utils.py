##################################
#
# Python API to Proxmox REST API
# See http://pve.proxmox.com/wiki/Proxmox_VE_API for details.
#
# Utility and helper functions for the lazy in all of us.
#
##################################


import re

from .nodes import Node
from .nodes import OpenVZ
from .exceptions import logcall

def find_nodes(connection):
    """
    Returns a list of Proxmox Node objects
    """
    nodes = []

    for node in connection.simple_fetch('nodes'):
        nodes.append(Node(connection, node['node']))

    return nodes

def find_vm_by_name(connection, hostname):
    """
    Searches on Proxmox for a list of available nodes.
    For each node retrieves the vm list and parses this
    until it is found and an OpenVZ instance can be returned.

    None is returned if the name is not found.
    ?Should it raise an exception instead?
    """
    for node in connection.simple_fetch('nodes'):
        for vm in connection.simple_fetch('nodes/%s/openvz' % node['node']):
            if re.match('^%s.london.baseblack.com' % hostname, vm['name']) or re.match(hostname, vm['name']):
                vm['node'] = node
                return OpenVZ(node, vm['vmid'])

def find_vm_by_id(connection, vmid):
    """
    Same as $find_vm_by_name, but with vmid as search parameter.
    """
    for node in connection.simple_fetch('nodes'):
        for vm in connection.simple_fetch('nodes/%s/openvz' % node['node']):
            if vmid == str(vm['vmid']):
                vm['node'] = node
                return OpenVZ(node, vm['vmid'])

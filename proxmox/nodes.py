##################################
#
# Python API to Proxmox REST API
# See http://pve.proxmox.com/wiki/Proxmox_VE_API for details.
#
# Object types based on Nodes.
#
##################################

import time
import re

from .proxmox import Proxmox
from .exceptions import logcall

class NodeBase(Proxmox):
    """
    A _virtual_ base class for nodes.
    """
    def __init__(self, connection, node):
        """"
        arguments: conn = proxmox.Connector() object with auth_token.
                   node = string/ip name of the node the vm lives on.
        """
        Proxmox.__init__(self, connection)
        self.node = node
        self.baseurl = "{0}/nodes/{1}".format(self.baseurl, self.node)

    def execute_task(self, filter, params={}, callback=None):
        """
        Used to perform POST requests which trigger Tasks on Proxmox which are
        expected to return after a period of time.

        Tasks are listed + accessed via the node interface which is the reasoning
        for placing this method here.

        WARNING: This is a blocking call and could take a long time to return.
        @TODO - Thread the status check loop and exec callback when done.
        @TODO - yield logs progressively
        """
        upid = self.post(filter, "")

        node = Node(self, self.node)
        status = node.tasks(upid).status().get('status')

        while status == 'running':
            time.sleep(1)
            status = node.tasks(upid).status().get('status')

        log = node.tasks(upid).log()
        status = node.tasks(upid).status()

        return status, [log[i]['t'] for i in range(0,len(log))]


class Node(NodeBase):
    def __init__(self, connection, node):
        """
        arguments: conn = proxmox.Connector() object with auth_token.
                   node = string/ip name of the node the vm lives on.
        """
        NodeBase.__init__(self, connection, node)

    # Methods defined for POST requests.
    def vncshell(self):
        return self.post('vncshell')

    def vzdump(self, **kwargs):
        return self.post('vzdump', kwargs)

    # Convenience constructor methods.
    def openvz(self, vmid):
        return OpenVZ(self, self.node, vmid)

    def tasks(self, upid):
        return Task(self, self.node, upid)


class OpenVZ(NodeBase):
    def __init__(self, conn, node, vmid):
        """
        arguments: conn = proxmox.Connector() object with auth_token.
                   node = string/ip name of the node the vm lives on.
                   vmid = the unique id of the vm.
        """
        NodeBase.__init__(self, conn, node)
        self.vmid = vmid
        self.baseurl = "{0}/openvz/{1}".format(self.baseurl, self.vmid)

    # Methods defined for task execution requests.
    def migrate(self, target, online=False, callback=None):
        """Migrate the container to another node. Creates a new mirgration task."""
        return self.execute_task('migrate', params={'target': target, 'online': online}, callback=callback)

    def mount(self, callback=None):
        """Mounts the container private area."""
        return self.execute_task('status/mount', callback=callback)

    def shutdown(self, forceStop=False, timeout=None, callback=None):
        """Shutdown the container."""
        params = {}
        if forceStop:
            params['forceStop'] = forceStop
        if timeout:
            params['timeout'] = timeout

        return self.execute_task('status/shutdown', params=params, callback=callback)

    def start(self, callback=None):
        """Start the container."""
        return self.execute_task('status/start', callback=callback)

    def stop(self, callback=None):
        """Stop the container."""
        return self.execute_task('status/stop', callback=callback)

    def umount(self, callback=None):
        """Unmounts the container private area."""
        return self.execute_task('status/umount', callback=callback)

    def vncproxy(self):
        """Creates a TCP VNC proxy connections."""
        return self.post('vncproxy')


class Qemu(NodeBase):
    def __init__(self, conn, node, vmid):
        """
        arguments: conn = proxmox.Connector() object with auth_token.
                   node = string/ip name of the node the vm lives on.
                   vmid = the unique id of the vm.
        """
        NodeBase.__init__(self, conn, node)
        self.vmid = vmid
        self.baseurl = "{0}/qemu/{1}".format(self.baseurl, self.vmid)

    # Methods defined for task execution requests.
    def migrate(self, target, online=False, callback=None):
        """Migrate the container to another node. Creates a new mirgration task."""
        return self.execute_task('migrate', params={'target': target, 'online': online}, callback=callback)

    def monitor(self, command, callback=None):
        """Execute Qemu monitor commands"""
        return self.execute_task('monitor', params={'target': target, 'online': online}, callback=callback)

    def reset(self, skiplock=False, callback=None):
        """Reset virtual machine."""
        return self.execute_task('status/reset', params={'skiplock': skiplock}, callback=callback)

    def resume(self, skiplock=False, callback=None):
        """Reset virtual machine."""
        if re.match("^root@(pve|pam)", self._auth.username):
            params = {'skiplock': skiplock}
        else:
            params = {}

        return self.execute_task('status/resume', params=params, callback=callback)

    def vncproxy(self):
        """Creates a TCP VNC proxy connections."""
        return self.post('vncproxy')

class Task(NodeBase):
    def __init__(self, connection, node, upid):
        """
        arguments: connection = proxmox.Connector() object with auth_token.
                   node = string/ip name of the node the vm lives on.
                   vmid = the unique id of the vm.
        """
        NodeBase.__init__(self, connection, node)
        self.upid = str(upid)
        self.baseurl = "{0}/tasks/{1}".format(self.baseurl, self.upid)

import logging

from proxmox import Connector
from proxmox import Node, OpenVZ

def test_create_OpenVZ_Object_FromNode():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)
    vm = node.openvz(VMID)  # VMID is a testing vm 'packages'

    assert isinstance(vm, OpenVZ)
    assert vm.vmid == VMID
    assert vm.baseurl == 'https://{0}:8006/api2/json/nodes/{0}/openvz/{1}'.format(PROXMOX_HOST,VMID)


def test_OpenVZ_status():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)
    vm = node.openvz(VMID)  # 108 is a testing vm 'packages'

    assert vm.status
    assert vm.status.current()

def test_OpenVZ_start():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)
    vm = node.openvz(VMID)  # 108 is a testing vm 'packages'

    assert vm.start()

def test_OpenVZ_stop():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)
    vm = node.openvz(VMID)  # 108 is a testing vm 'packages'

    assert vm.stop()

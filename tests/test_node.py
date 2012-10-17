import logging

from proxmox import Connector
from proxmox import Node
from proxmox.exceptions import ProxmoxError

def test_create_Node_object():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert isinstance(node, Node)
    assert node.node == PROXMOX_HOST
    assert node.baseurl == 'https://{0}:8006/api2/json/nodes/{0}'.format(PROXMOX_HOST)

def test_Node_dns():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.dns()

def test_Node_rrd():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.rrd(ds='cpu',timeframe='hour')

def test_Node_rrddata():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.rrddata(timeframe='hour')

def test_Node_status():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.status()

def test_Node_subscription():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.subscription()

def test_Node_syslog():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.syslog()

def test_Node_time():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.time()

def test_Node_ubcfailcnt():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.ubcfailcnt()

def test_Node_version():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.version()

def test_Node_vncshell():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.vncshell()

def test_Node_vzdump():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    assert node.vzdump(vmid=108, stdout=True, compress='gzip')

def test_Node_raiseExceptionOnUndefined():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"
    VMID = 108

    connection = Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = Node(connection, PROXMOX_HOST)

    try:
        node.failme()
    except ProxmoxError as e:
        logging.debug(e)
        assert True
        return

    assert False


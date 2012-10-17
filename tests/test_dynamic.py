import proxmox
import logging

def testUndefinedMethod():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"

    connection = proxmox.Connector(PROXMOX_HOST, PROXMOX_PORT)
    connection.fetch_auth_token(USER, PASSWD)

    node = proxmox.Node(connection, PROXMOX_HOST)
    logging.debug('node is %s' % node)

    version = node.version()  # UNDEFINED METHOD .version() dynamically generated
    logging.debug(version)

    assert isinstance(version, dict)


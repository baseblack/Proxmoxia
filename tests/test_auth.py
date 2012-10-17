# Connection and authentication tests
from nose import *
import proxmox

def setup_func():
    """function level setup function"""

def teardown_func():
    """function level teardown function"""

@with_setup(setup_func)
def testAuth():
    PROXMOX_HOST = "proxmox-7"
    PROXMOX_PORT = 8006
    USER = "apiuser@pam"
    PASSWD = "strawberries"

    connection = proxmox.Connector(PROXMOX_HOST, PROXMOX_PORT)
    assert connection.fetch_auth_token(USER, PASSWD)

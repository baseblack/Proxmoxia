##################################
#
# Python API to Proxmox REST API
# See http://pve.proxmox.com/wiki/Proxmox_VE_API for details.
#
# __author__ = "Andrew Bunday"
#
##################################

import logging

# Exceptions
class ProxmoxError(BaseException):
    # @TODO add logging.
    pass

class ProxmoxAuthError(ProxmoxError):
    # @TODO add logging.
    pass

class ProxmoxConnectionError(ProxmoxError):
    # @TODO add logging.
    pass

class ProxmoxTypeError(TypeError):
    # @TODO add logging.
    pass


# Logger decorator.
def logcall(func):
    """
    Debug logging decorator.
    """
    def newfunc(*args, **kwargs):
        #@TODO flesh this out a bit.
        logging.debug("%s func called with args '...'" % (func.__name__))
        logging.debug(args)
        logging.debug(kwargs)
        return func(*args, **kwargs)

    return newfunc

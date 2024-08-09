class VNodeError(Exception):
    """Base (catch-all) VNode exception"""

class NotConnectedVNodesError(VNodeError):
    """Two nodes are not connected"""
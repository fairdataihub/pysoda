from pennsieve2.pennsieve import Pennsieve
from .exceptions import PennsieveAgentError

def connect_pennsieve_client(account_name):
    """
        Connects to Pennsieve Python client to the Agent and returns the initialized Pennsieve object.
    """
    try:
        return Pennsieve(profile_name=account_name)
    except Exception as e:
        raise PennsieveAgentError(f"Could not connect to the Pennsieve agent: {e}")
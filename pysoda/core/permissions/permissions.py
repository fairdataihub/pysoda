import requests
from constants import PENNSIEVE_URL

def pennsieve_get_current_user_permissions(dataset_id, ps_or_token):

    if type(ps_or_token) is str:
        access_token = ps_or_token
    else:
        access_token = ps_or_token.get_user().session_token

    r = requests.get(f"{PENNSIEVE_URL}/datasets/{dataset_id}/role", headers={"Authorization": f"Bearer {access_token}"})
    r.raise_for_status()

    return r.json()
import os
import requests
from urllib.parse import urlencode


STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"


def get_login_url(domain):

    domain = domain.rstrip("/")

    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",

        "openid.mode": "checkid_setup",

        "openid.return_to":
            f"{domain}/auth/steam/callback",

        "openid.realm":
            domain,

        "openid.identity":
            "http://specs.openid.net/auth/2.0/identifier_select",

        "openid.claimed_id":
            "http://specs.openid.net/auth/2.0/identifier_select"
    }

    return (
        STEAM_OPENID_URL
        + "?"
        + urlencode(params)
    )



def verify_steam(data):

    verification = {}

    for key, value in data.items():

        if key.startswith("openid"):
            verification[key] = value


    verification["openid.mode"] = "check_authentication"


    try:

        response = requests.post(
            STEAM_OPENID_URL,
            data=verification,
            timeout=10
        )

        return "is_valid:true" in response.text


    except Exception:

        return False




def get_steam_id(identity):

    return identity.rstrip("/").split("/")[-1]




def get_profile(steam_id):

    api_key = os.getenv(
        "STEAM_API_KEY"
    )


    if not api_key:
        return None


    url = (
        "https://api.steampowered.com/"
        "ISteamUser/GetPlayerSummaries/v2/"
    )


    params = {

        "key": api_key,

        "steamids": steam_id

    }


    response = requests.get(
        url,
        params=params,
        timeout=10
    )


    data = response.json()


    players = (
        data
        .get("response", {})
        .get("players", [])
    )


    if not players:
        return None


    player = players[0]


    return {

        "steamid":
            player.get("steamid"),

        "name":
            player.get("personaname"),

        "avatar":
            player.get("avatarfull"),

        "profile":
            player.get("profileurl")

    }
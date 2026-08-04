import os
import requests
from urllib.parse import urlencode


STEAM_OPENID = "https://steamcommunity.com/openid/login"


def get_login_url(domain):

    params = {

        "openid.ns":
        "http://specs.openid.net/auth/2.0",

        "openid.mode":
        "checkid_setup",

        "openid.return_to":
        f"{domain}/auth/steam/callback",

        "openid.realm":
        domain,

        "openid.identity":
        "http://specs.openid.net/auth/2.0/identifier_select",

        "openid.claimed_id":
        "http://specs.openid.net/auth/2.0/identifier_select"

    }

    return STEAM_OPENID + "?" + urlencode(params)



def verify_steam(response):

    data = {}

    for key, value in response.items():

        if key.startswith("openid"):
            data[key] = value


    data["openid.mode"] = "check_authentication"


    r = requests.post(
        STEAM_OPENID,
        data=data
    )


    return "is_valid:true" in r.text



def get_steam_id(identity):

    return identity.split("/")[-1]



def get_profile(steam_id):

    key = os.getenv("STEAM_API_KEY")


    url = (
        "https://api.steampowered.com/"
        "ISteamUser/GetPlayerSummaries/v2/"
    )


    params = {

        "key": key,
        "steamids": steam_id

    }


    r = requests.get(
        url,
        params=params
    )


    data = r.json()


    player = data["response"]["players"][0]


    return {

        "steamid": player["steamid"],
        "name": player["personaname"],
        "avatar": player["avatarfull"],
        "profile": player["profileurl"]

    }
import os
import requests
from urllib.parse import urlencode


STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"


def get_login_url(domain: str) -> str:
    """
    Genera la URL de autenticación OpenID de Steam.
    """

    domain = domain.rstrip("/")

    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": f"{domain}/auth/steam/callback",
        "openid.realm": domain,
        "openid.identity": (
            "http://specs.openid.net/auth/2.0/identifier_select"
        ),
        "openid.claimed_id": (
            "http://specs.openid.net/auth/2.0/identifier_select"
        )
    }

    return f"{STEAM_OPENID_URL}?{urlencode(params)}"



def verify_steam(response_data) -> bool:
    """
    Verifica que la respuesta enviada por Steam sea válida.
    """

    verification_data = {
        key: value
        for key, value in response_data.items()
        if key.startswith("openid")
    }

    verification_data["openid.mode"] = "check_authentication"


    try:

        response = requests.post(
            STEAM_OPENID_URL,
            data=verification_data,
            timeout=10
        )

        return "is_valid:true" in response.text


    except requests.RequestException:

        return False




def extract_steam_id(identity_url: str) -> str:
    """
    Extrae el SteamID64 desde la URL OpenID.
    """

    return identity_url.rstrip("/").split("/")[-1]




def get_profile(steam_id: str) -> dict:
    """
    Obtiene información pública del usuario usando Steam Web API.
    """

    api_key = os.getenv("STEAM_API_KEY")


    if not api_key:
        raise Exception(
            "STEAM_API_KEY no configurada"
        )


    endpoint = (
        "https://api.steampowered.com/"
        "ISteamUser/GetPlayerSummaries/v2/"
    )


    params = {
        "key": api_key,
        "steamids": steam_id
    }


    response = requests.get(
        endpoint,
        params=params,
        timeout=10
    )


    response.raise_for_status()


    data = response.json()


    players = data.get(
        "response",
        {}
    ).get(
        "players",
        []
    )


    if not players:
        return None


    player = players[0]


    return {
        "steamid": player.get("steamid"),
        "name": player.get("personaname"),
        "avatar": player.get("avatarfull"),
        "profile": player.get("profileurl")
    }
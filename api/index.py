import os

from flask import (
    Flask,
    render_template,
    redirect,
    session,
    request
)

from steam import (
    get_login_url,
    verify_steam,
    get_steam_id,
    get_profile
)



# ==============================
# CONFIGURACIÓN DEMO
# ==============================

SECRET_KEY = "b714d146b273ca762ea48404f6551ee271c25bd3e32a7ef0d4b4d3855627fe6e"

STEAM_API_KEY = "483B8596662FC2F74C8C0E0D990A75F1"

DOMAIN = "https://skinshop-pw3waptrf-tobias-projects-3446f3a7.vercel.app"



# Guardamos la API KEY para steam.py
os.environ["STEAM_API_KEY"] = STEAM_API_KEY



# ==============================
# FLASK
# ==============================

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


app.secret_key = SECRET_KEY



print("==========================")
print("STEAM LOGIN")
print("DOMAIN:", DOMAIN)
print("==========================")



# ==============================
# HOME
# ==============================

@app.route("/")
def home():

    return render_template(
        "index.html",
        user=session.get("user")
    )



# ==============================
# LOGIN STEAM
# ==============================

@app.route("/login")
def login():

    try:

        steam_login_url = get_login_url(
            DOMAIN
        )

        print(
            "STEAM LOGIN URL:",
            steam_login_url
        )


        return redirect(
            steam_login_url
        )


    except Exception as error:

        print(
            "LOGIN ERROR:",
            error
        )

        return "Error creando login Steam"



# ==============================
# CALLBACK STEAM
# ==============================

@app.route("/auth/steam/callback")
def steam_callback():

    try:


        print(
            "STEAM RESPONSE:",
            request.args
        )


        valid = verify_steam(
            request.args
        )


        if not valid:

            return "Steam verification failed"



        identity = request.args.get(
            "openid.claimed_id"
        )


        if not identity:

            return "Steam ID not found"



        steam_id = get_steam_id(
            identity
        )


        print(
            "STEAM ID:",
            steam_id
        )


        user = get_profile(
            steam_id
        )


        if not user:

            return "Steam profile error"



        session["user"] = user



        return redirect("/")



    except Exception as error:


        print(
            "CALLBACK ERROR:",
            error
        )


        return "Steam callback error"




# ==============================
# LOGOUT
# ==============================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")



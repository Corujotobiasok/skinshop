import os

from flask import (
    Flask,
    render_template,
    redirect,
    session,
    request
)

from dotenv import load_dotenv


# Import para Vercel
from steam import (
    get_login_url,
    verify_steam,
    get_steam_id,
    get_profile
)


load_dotenv()


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


app.secret_key = os.getenv(
    "SECRET_KEY",
    "default-secret-key-change-this"
)


DOMAIN = os.getenv(
    "DOMAIN",
    "http://127.0.0.1:5000"
)


print("STEAM DOMAIN:", DOMAIN)



@app.route("/")
def home():

    return render_template(
        "index.html",
        user=session.get("user")
    )



@app.route("/login")
def login():

    try:

        steam_url = get_login_url(
            DOMAIN
        )

        return redirect(
            steam_url
        )


    except Exception as e:

        print(
            "LOGIN ERROR:",
            e
        )

        return "Error creando login de Steam"



@app.route("/auth/steam/callback")
def steam_callback():

    try:

        if not verify_steam(request.args):

            return "Steam verification failed"



        identity = request.args.get(
            "openid.claimed_id"
        )


        if not identity:

            return "Steam ID missing"



        steam_id = get_steam_id(
            identity
        )


        user = get_profile(
            steam_id
        )


        if not user:

            return "Could not get Steam profile"



        session["user"] = user


        return redirect("/")


    except Exception as e:

        print(
            "STEAM CALLBACK ERROR:",
            e
        )

        return "Steam callback error"



@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
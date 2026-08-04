import os

from flask import (
    Flask,
    render_template,
    redirect,
    session,
    request
)

from dotenv import load_dotenv

from .steam import (
    get_login_url,
    verify_steam,
    get_steam_id,
    get_profile
)


load_dotenv()


app = Flask(
    __name__,
    template_folder="../templates"
)


app.secret_key = os.getenv(
    "SECRET_KEY"
)


DOMAIN = os.getenv(
    "DOMAIN"
)



@app.route("/")
def index():

    return render_template(
        "index.html",
        user=session.get("user")
    )



@app.route("/login")
def login():

    return redirect(
        get_login_url(DOMAIN)
    )



@app.route("/auth/steam/callback")
def steam_callback():


    if not verify_steam(request.args):

        return "Steam authentication failed"


    steam_id = get_steam_id(
        request.args["openid.claimed_id"]
    )


    user = get_profile(
        steam_id
    )


    session["user"] = user


    return redirect("/")



@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")



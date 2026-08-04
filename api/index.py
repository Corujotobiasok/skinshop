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
    template_folder="../templates",
    static_folder="../static"
)


app.secret_key = os.getenv(
    "SECRET_KEY"
)


DOMAIN = os.getenv(
    "DOMAIN"
)



@app.route("/")
def home():

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

        return "User data error"



    session["user"] = user


    return redirect("/")




@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

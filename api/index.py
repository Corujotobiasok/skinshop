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
    create_login_url,
    validate_login,
    get_steam_id,
    get_user
)



load_dotenv()



app = Flask(
    __name__,
    template_folder="../templates"
)



app.secret_key = os.getenv(
    "SECRET_KEY",
    "demo-secret-key"
)



DOMAIN = os.getenv(
    "DOMAIN"
)



@app.route("/")
def index():

    if "user" in session:

        return redirect("/dashboard")


    return render_template(
        "index.html"
    )



@app.route("/login")
def login():

    login_url = create_login_url(
        DOMAIN
    )

    return redirect(
        login_url
    )



@app.route("/auth/steam/callback")
def steam_callback():


    if not validate_login(
        request.args
    ):

        return "Steam authentication failed"



    identity = request.args.get(
        "openid.claimed_id"
    )


    if not identity:

        return "Steam ID missing"



    steam_id = get_steam_id(
        identity
    )



    user = get_user(
        steam_id
    )


    if not user:

        return "Steam user not found"



    session["user"] = user



    return redirect(
        "/dashboard"
    )





@app.route("/dashboard")
def dashboard():


    if "user" not in session:

        return redirect(
            "/login"
        )


    return render_template(
        "dashboard.html",
        user=session["user"]
    )





@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        "/"
    )
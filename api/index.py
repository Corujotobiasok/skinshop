import os

from flask import (
    Flask,
    render_template,
    redirect,
    session,
    url_for
)

from dotenv import load_dotenv

load_dotenv()

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():

    return render_template(
        "index.html",
        user=session.get("user")
    )


@app.route("/login")
def login():

    # Más adelante aquí redireccionaremos a Steam
    return redirect("/auth/steam")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


app = app
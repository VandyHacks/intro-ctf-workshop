from flask import Flask, render_template, session, redirect, request
from flask_session import Session

app = Flask(__name__)
app.secret_key = "secret"
app.config["SESSION_USE_SIGNER"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# bc honestly why would I use SQL for any of this
# if I wasn't intentionally making vulns
profiles = {"nisala": "Check out my cool profile!"}


@app.before_request
def check_username_set():
    if "username" not in session and request.path not in ["/", "/setusername"]:
        return redirect("/")

@app.route("/")
def index():
    if "username" in session:
        return redirect("/profile")

    return render_template("set_username.html")

@app.post("/setusername")
def set_username():
    username = request.form.get("username")
    if username is None or username.strip() == "":
        return "Username not provided"

    if username in session:
        return redirect("/profile")

    if username in profiles:
        return "Username already taken"

    session["username"] = username
    return redirect("/profile")

@app.route("/profile")
def profile():
    username = session["username"]
    return render_template("my_profile.html", username=username, profile=profiles.get(username, "No profile found"))

@app.post("/update_profile")
def update_profile():
    username = session["username"]
    profile = request.form.get("profile")
    profiles[username] = profile
    return redirect("/profile")

@app.route("/profile/<username>")
def other_profile(username):
    return render_template("other_profile.html", username=username, profile=profiles.get(username, "No profile found"))
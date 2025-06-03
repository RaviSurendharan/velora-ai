from flask import Blueprint, render_template, request, redirect, url_for, session
import database.models as db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]
        escort = db.get_escort(phone)
        if escort and escort["password"] == password:
            session["escort_phone"] = phone
            return redirect(url_for("dashboard"))
        return "Invalid credentials", 401
    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        password = request.form["password"]
        escort = db.create_escort(name, phone, password)
        session["escort_phone"] = phone
        return redirect(url_for("dashboard"))
    return render_template("signup.html")

@auth_bp.route("/logout")
def logout():
    session.pop("escort_phone", None)
    return redirect(url_for("auth.login"))


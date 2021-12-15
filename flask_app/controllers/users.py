from flask_app import app
from flask import render_template, redirect, flash, request, session
from flask_app.models import user, recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")                             # "/" INDEX
def index():
    return render_template("index.html")
                                            # REGISTER NEW USER
@app.route("/register", methods=["POST"])
def create_user():
    if not user.User.validate_registration(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    } 

    new_user_id = user.User.create_user(data)
    session["user_id"] = new_user_id
    return redirect("/dashboard")

@app.route("/dashboard")                # /DASHBOARD
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data_user = {
        "id": session["user_id"]
    }
    user_in_session = user.User.get_user_by_id(data_user)
    all_recipes = recipe.Recipe.get_all_recipes()

    delete_list = user.User.can_delete(user_in_session, all_recipes)
    edit_list = user.User.can_edit(user_in_session, all_recipes)


    return render_template("dashboard.html", user = user_in_session, all_recipes = all_recipes, delete_list = delete_list, edit_list = edit_list)










@app.route("/login", methods=["POST"])  # /LOGIN
def login():
    if not user.User.validate_login(request.form):
        return redirect("/")

    data = {
        "email": request.form["email"]
    }
    user_from_db = user.User.get_user_by_email(data)
    if not user_from_db:
        flash("Invalid email or password", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user_from_db.password, request.form["password"]):
        flash("Invalid email or password", "login")
        return redirect("/")

    session["user_id"] = user_from_db.id

    all_recipes = recipe.Recipe.get_all_recipes()
    return redirect("/dashboard")


@app.route("/logout")           # /LOGOUT
def logout():
    session.clear()
    return redirect("/")
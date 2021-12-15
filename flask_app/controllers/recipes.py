from flask_app import app
from flask import render_template, redirect, flash, request, session
from flask_app.models import recipe

@app.route("/recipes/new")                  # ADD RECIPE PAGE
def recipes_new():
    if "user_id" not in session:
        return redirect("/")
    return render_template("recipes_new.html")

@app.route("/create_recipe", methods=["POST"])  # ADD RECIPE ACTION
def create_recipe():

    if not recipe.Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")

    recipe_data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30": request.form["under_30"],
        "user_id": session['user_id']
    }
    new_recipe = recipe.Recipe.create_recipe(recipe_data)
    return redirect("/dashboard")

@app.route("/recipes/<id>")
def view_recipe(id):
    recipe_id = {
        "id": id
    }
    get_recipe = recipe.Recipe.get_recipe_by_id(recipe_id)
    return render_template("recipe.html", recipe = get_recipe)

@app.route("/delete_recipe/<id>")
def delete_recipe(id):
    data = {
        "id": id
    }
    get_recipe = recipe.Recipe.get_recipe_by_id(data) #CHECK IF SESSION USER IS DOING THIS INSTEAD OF SOMEBODY USING THE INSPECTOR WINDOW
    if session["user_id"] != get_recipe.user_id:
        session.clear()
        return redirect("/")
        
    deleted_recipe = recipe.Recipe.delete_recipe(data)
    return redirect("/dashboard") 

@app.route("/edit_recipe/<id>")
def edit_recipe(id):
    data = {
        "id": id
    }
    get_recipe = recipe.Recipe.get_recipe_by_id(data) #CHECK IF SESSION USER IS DOING THIS INSTEAD OF SOMEBODY USING THE INSPECTOR WINDOW
    if session["user_id"] != get_recipe.user_id:
        session.clear()
        return redirect("/")
    return render_template("edit_recipe.html", recipe = get_recipe) 

@app.route("/update_recipe/<id>", methods=["POST"])
def update_recipe(id):
    recipe_id = {
        "id": id
    }
    get_recipe = recipe.Recipe.get_recipe_by_id(recipe_id)
    recipe_data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30": request.form["under_30"],
        "user_id": session['user_id'],
        "id": id
    }
    if len(recipe_data["name"]) == 0:
        recipe_data["name"] = get_recipe.name
    if len(recipe_data["instructions"]) == 0:
        recipe_data["instructions"] = get_recipe.instructions
    if len(recipe_data["description"]) == 0:
        recipe_data["description"] = get_recipe.description

    new_recipe = recipe.Recipe.update_recipe(recipe_data)
    return redirect("/dashboard")

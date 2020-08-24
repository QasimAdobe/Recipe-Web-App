from flask import (
    Blueprint,
    render_template,
    url_for,
    request,
    redirect,
    flash,
)
from App.models import (
    User,
    Recipe,
    Ingredient,
)
from App import db
from App.forms import (
    UpdateProfileForm,
    RecipeForm,
)
from Controls import PassiveControls
user = Blueprint("user", __name__, static_folder="static", template_folder="templates")


@user.route('/')
def index():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        return render_template('user/index.html', user=valid[3])
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/profile')
def profile():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        user_data = User.query.get_or_404(valid[1])
        recipe = Recipe.query.filter_by(created_by=valid[1]).all()
        return render_template('user/profile.html', user=valid[3], profile=user_data, recipes=recipe)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/edit/profile', methods=["POST", "GET"])
def edit_profile():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        user = User.query.get_or_404(valid[1])
        form = UpdateProfileForm()
        if request.method == "POST":
            if form.image.data:
                image_file = PassiveControls.save_file(form.image.data)
                user.profile_pic = image_file
            user.name = form.name.data
            user.username = form.username.data
            user.email = form.email.data
            db.session.commit()
            return redirect(url_for('user.profile'))
        elif request.method == "GET":
            form.name.data = user.name
            form.username.data = user.username
            form.email.data = user.email
            form.designation.data = user.designation
            return render_template('user/edit_profile.html', user=valid[3], form=form)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/chefs')
def cooks():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        users = User.query.filter_by(type="user").all()
        return render_template('user/cooks.html', user=valid[3], users=users)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/chef/<int:user_id>')
def user_profile(user_id):
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        user_data = User.query.get_or_404(user_id)
        recipe = Recipe.query.filter_by(created_by=valid[1]).all()
        return render_template('user/user_profile.html', user=valid[3], profile=user_data, recipes=recipe)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/ingredients')
def ingredients():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        ingredient = Ingredient.query.all()
        return render_template('user/ingredients.html', user=valid[3], ingredients=ingredient)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/saved')
def saved():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        return render_template('user/saved.html', user=valid[3])
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/publish', methods=["POST", "GET"])
def publish_recipe():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        form = RecipeForm()
        if form.validate_on_submit():
            if form.image.data:
                image_file = PassiveControls.save_file(form.image.data)
            recipe = Recipe(title=form.title.data, description=form.description.data,time=form.time.data,
                            servings=form.servings.data, ingredients=form.ingredients.data, image=image_file,
                            approval="-1", status="0", created_by=valid[1])
            db.session.add(recipe)
            db.session.commit()
            flash("Recipe has been published, please wait till its approved by our team.", "success")
            return redirect(url_for('user.index'))
        return render_template('user/publish.html', user=valid[3], form=form)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/recipes')
def recipes():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        recipe = Recipe.filter_by(approval=1).query.all()
        return render_template('user/recipes.html', user=valid[3], recipes=recipe)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/recipe/<int:recipe_id>')
def single_recipe(recipe_id):
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        recipe = Recipe.query.get_or_404(recipe_id)
        return render_template('user/single.html', user=valid[3], recipes=recipe)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)



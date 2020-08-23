from flask import (
    Blueprint,
    render_template,
    url_for,

)
from App.models import (
    User,
    Recipe,
)
from Controls import LoginControl
user = Blueprint("user", __name__, static_folder="static", template_folder="templates")


@user.route('/')
def index():
    valid = LoginControl.validation()
    if valid[0] and valid[2] == "user":
        return render_template('user/index.html', user=valid[3])
    else:
        return render_template("error.html", error=LoginControl.ErrMsg.access)


@user.route('/profile')
def profile():
    valid = LoginControl.validation()
    if valid[0] and valid[2] == "user":
        user_data = User.query.get_or_404(valid[1])
        recipe = Recipe.query.filter_by(created_by=valid[1]).all()
        return render_template('user/profile.html', user=valid[3], profile=user_data, recipes=recipe)
    else:
        return render_template("error.html", error=LoginControl.ErrMsg.access)


@user.route('/edit/profile')
def edit_profile():
    valid = LoginControl.validation()
    if valid[0] and valid[2] == "user":
        return render_template('user/edit_profile.html', user=valid[3])
    else:
        return render_template("error.html", error=LoginControl.ErrMsg.access)


@user.route('/recipes')
def recipes():
    valid = LoginControl.validation()
    if valid[0] and valid[2] == "user":
        return render_template('user/recipes.html', user=valid[3])
    else:
        return render_template("error.html", error=LoginControl.ErrMsg.access)


@user.route('/cooks')
def cooks():
    valid = LoginControl.validation()
    if valid[0] and valid[2] == "user":
        return render_template('user/cooks.html', user=valid[3])
    else:
        return render_template("error.html", error=LoginControl.ErrMsg.access)


@user.route('/saved')
def saved():
    valid = LoginControl.validation()
    if valid[0] and valid[2] == "user":
        return render_template('user/saved.html', user=valid[3])
    else:
        return render_template("error.html", error=LoginControl.ErrMsg.access)


@user.route('/publish')
def publish_recipe():
    valid = LoginControl.validation()
    if valid[0] and valid[2] == "user":
        return render_template('user/publish.html', user=valid[3])
    else:
        return render_template("error.html", error=LoginControl.ErrMsg.access)

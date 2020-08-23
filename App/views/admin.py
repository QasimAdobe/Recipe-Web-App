from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from Controls import PassiveControls
from App.models import (
    User,
)
from App import db, bcrypt
from App.forms import (
    RegisterForm,
)


admin = Blueprint("admin", __name__, static_folder="static", template_folder="/templates")


@admin.route('/')
def index():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "admin":
        return render_template('admin/index.html', user=valid[3])
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@admin.route('/users')
def users():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "admin":
        users = User.query.all()
        return render_template('admin/users.html', user=valid[3], user_data=users)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@admin.route('/users/add', methods=["POST", "GET"])
def add_user():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "admin":
        form = RegisterForm()
        if request.method == "POST":
            if form.image.data:
                image_file = PassiveControls.save_file(form.image.data)
            hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(name=form.name.data, username=form.username.data, email=form.email.data, password= hashed_pass,
                        type= form.type.data, designation=form.designation.data, profile_pic=image_file)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('admin.users'))
        return render_template('admin/add_user.html', user=valid[3], form=form)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@admin.route('/user/<int:user_id>')
def user_profile(user_id):
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "admin":
        user_data = User.query.get_or_404(user_id)
        return render_template('admin/user_profile.html',user=valid[3], profile=user_data)
    else:
        return render_template("main/error.html", error=PassiveControls.ErrMsg.access)


@admin.route('/suspend/<int:user_id>')
def suspend_user(user_id):
    valid = PassiveControls.validation()
    user = User.query.get_or_404(user_id)
    if valid[0] and valid[2] == "admin":
        if user_id != valid[1]:
            user.type = "suspended"
            db.session.commit()
            flash("User's Access Has been suspended!", "info")
        else:
            flash("You can't suspend your own ID", "info")
        return redirect(url_for('admin.users'))
    else:
        return render_template("main/error.html", error=PassiveControls.ErrMsg.access)


@admin.route('/delete/<int:user_id>')
def delete_user(user_id):
    valid = PassiveControls.validation()
    user = User.query.get_or_404(user_id)
    if valid[0] and valid[2] == "admin":
        if user_id != valid[1]:
            db.session.delete(user)
            db.session.commit()
            flash("User has been deleted!", "info")
        else:
            flash("You can't delete your own ID", "info")
        return redirect(url_for('admin.users'))
    else:
        return render_template("main/error.html", error=PassiveControls.ErrMsg.access)

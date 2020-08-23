from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from App.views.admin import admin
from App.views.user import user
from App import (
    app,
    bcrypt,
    db,
)
from App.forms import (
    LoginForm,
    RegisterForm,
)
from App.models import (
    User,
)
from Controls import LoginControl

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(user, url_prefix="/user")


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error=e)


@app.route('/')
def index():
    valid = LoginControl.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.index'))
    else:
        return render_template('unlogged/index.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    valid = LoginControl.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.index'))
    else:
        form = RegisterForm()
        if request.method == "POST":
            hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(name=form.name.data, username=form.username.data, email=form.email.data, password= hashed_pass, type= "user", designation="Chef")
            db.session.add(user)
            db.session.commit()
            flash('Account has been created!', 'success')
            LoginControl.add_session(user.id, user.type, user.name, None)
            return redirect(url_for('user.index'))
        return render_template('unlogged/register.html', form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    valid = LoginControl.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.index'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                LoginControl.add_session(user.id, user.type, user.name, form.remember.data)
                if user.type == "admin":
                    return redirect(url_for('admin.index'))
                elif user.type == "user":
                    return redirect(url_for('user.index'))
                else:
                    flash('Your account access has been suspended!', 'info')
            else:
                flash('Username and Password does not match our database!', 'info')
        return render_template('unlogged/login.html', form=form)


@app.route('/logout')
def logout():
    valid = LoginControl.validation()
    if valid[0]:
        LoginControl.pop_session()
        flash("You have been logged out!")
        return redirect(url_for('.login'))
    else:
        flash("You're already logged out!", "info")
        return redirect(url_for('.login'))


@app.route('/recipes')
def recipes():
    valid = LoginControl.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.recipes'))
    else:
        return render_template('unlogged/recipes.html')


@app.route('/cooks')
def cooks():
    valid = LoginControl.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.cooks'))
    else:
        return render_template('unlogged/cooks.html')


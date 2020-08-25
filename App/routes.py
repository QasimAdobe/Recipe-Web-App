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
    Ingredient,
    Recipe,
)
from Controls import PassiveControls

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(user, url_prefix="/user")


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error=e)


@app.route('/install')
def install():
    try:
        user = User.query.get_or_404(1)
        return redirect(url_for('index'))
    except :
        db.create_all()
        hashed_pass = bcrypt.generate_password_hash("admin").decode('utf-8')
        user = User(name="Admin", username="admin", email="admin@admin.com", password=hashed_pass,
                    type="admin",
                    designation="Admin")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/')
def index():
    valid = PassiveControls.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.index'))
    else:
        editor_recipe = Recipe.query.filter_by(status=1).all()
        featured = Recipe.query.filter_by(status=2)
        users = User.query.filter_by(type="user").paginate(per_page=3)
        return render_template('unlogged/index.html', editor_recipe=editor_recipe, featured=featured, users=users)


@app.route('/soon')
def coming_soon():
    return render_template("error.html", error="This Feature is not available at this moment!")


@app.route('/register', methods=["POST", "GET"])
def register():
    valid = PassiveControls.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.index'))
    else:
        form = RegisterForm()
        if request.method == "POST":
            if form.image.data:
                image_file = PassiveControls.save_file(form.image.data)
            hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(name=form.name.data, username=form.username.data, email=form.email.data, password= hashed_pass, type= "user",
                        designation=form.designation.data, profile_pic=image_file)
            db.session.add(user)
            db.session.commit()
            PassiveControls.add_session(user.id, user.type, user.name, None)
            return redirect(url_for('user.index'))
        return render_template('unlogged/register.html', form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    valid = PassiveControls.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.index'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                PassiveControls.add_session(user.id, user.type, user.name, form.remember.data)
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
    valid = PassiveControls.validation()
    if valid[0]:
        PassiveControls.pop_session()
        flash("You have been logged out!")
        return redirect(url_for('.login'))
    else:
        flash("You're already logged out!", "info")
        return redirect(url_for('.login'))


@app.route('/recipes')
def recipes():
    valid = PassiveControls.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.recipes'))
    else:
        page = request.args.get('page', 1, type=int)
        recipe = Recipe.query.filter_by(approval=-1 and 1).paginate(page=page, per_page=5)
        return render_template('unlogged/recipes.html', recipes=recipe)


@app.route('/recipe/<int:recipe_id>')
def single_recipe(recipe_id):
    valid = PassiveControls.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.recipes'))
    else:
        recipe = Recipe.query.get_or_404(recipe_id)
        featured = Recipe.query.filter_by(status=1 and 2)
        ingredient = recipe.ingredients.split(',')
        return render_template('unlogged/single.html', user=valid[3], recipe=recipe, featured=featured, ingredients=ingredient)


@app.route('/chefs')
def cooks():
    valid = PassiveControls.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.cooks'))
    else:
        page = request.args.get('page', 1, type=int)
        users = User.query.filter_by(type="user").paginate(page=page, per_page=5)
        return render_template('unlogged/cooks.html', users=users)


@app.route('/chef/<int:user_id>')
def user_profile(user_id):
    valid = PassiveControls.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.index'))
    else:
        user_data = User.query.get_or_404(user_id)
        recipe = Recipe.query.filter_by(created_by=valid[1]).all()
        return render_template('unlogged/user_profile.html',user=valid[3], profile=user_data, recipes=recipe)


@app.route('/ingredients')
def ingredients():
    valid = PassiveControls.validation()
    if valid[0]:
        return redirect(url_for(f'{valid[2]}.ingredients'))
    else:
        page = request.args.get('page', 1, type=int)
        ingredient = Ingredient.query.paginate(page=page, per_page=6)
        return render_template('unlogged/ingredients.html', ingredients=ingredient)


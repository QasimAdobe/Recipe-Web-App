from flask import (
    Blueprint,
    render_template,

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

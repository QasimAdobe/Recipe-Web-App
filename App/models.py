from App import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default_user.jpg')
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_pic}', '{self.address}, '{self.phone}')"

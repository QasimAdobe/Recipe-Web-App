from flask import session


def validation():
    if "id" and "access" and "name" in session:
        return True, session['id'], session['access'], session['name']
    else:
        return False, "None", "None", "None"


def add_session(user_id, access, name, remember):
    if remember:
        session.permanent = True
        session['id'] = user_id
        session['access'] = access
        session['name'] = name
    else:
        session['id'] = user_id
        session['access'] = access
        session['name'] = name
    return True


def pop_session():
    session.pop('id', None)
    session.pop('access', None)
    session.pop('name', None)
    return True


class ErrMsg:
    access = "You don't have permission to view this page"

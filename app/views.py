from flask import jsonify, request
from app import app, db, oauth
from app.forms import RegistrationForm
from app.models import User


@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        # Not hashing the password, just a test app
        user = User(username=form.username.data, password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(
                {
                    'status': 'Success',
                    'message': str(user)
                }
            )
        except Exception as e:
            return jsonify(
                {
                    'status': 'Failure',
                    'error': str(e)
                }
            ), 400
    else:
        return jsonify(form.errors), 400


# OAuth based login views

@app.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def token_handler():
    return None

@app.route('/protected', methods=['GET'])
@oauth.require_oauth('email')
def haha():
    return jsonify(
        {'message': 'Yo OAuth2.0 Rocks', 'user': str(request.oauth.user)}
    ), 200
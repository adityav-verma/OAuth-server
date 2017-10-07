from flask import jsonify, request
from app import app, db
from app.forms import RegistrationForm
from app.models import User


@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        # Not hashing the password, just a test app
        user = User(name=form.name.data, password=form.password.data)
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

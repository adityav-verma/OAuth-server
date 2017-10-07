from app import app, db, oauth
from app.models import User, Client, Grant
from datetime import datetime, timedelta


def get_current_user():
    # Change impelementation to get the verified user
    return User.query.all()[0]

@oauth.clientgetter
def load_client(client_id):
    return Client.query.get(client_id)

@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()

@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    expires = datetime.utcnow() + timedelta(seconds=60)

    # The params will be sent when client makes a request
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=get_current_user(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant
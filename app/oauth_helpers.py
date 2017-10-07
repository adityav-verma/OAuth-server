from app import app, db, oauth
from app.models import User, Client, Grant, Token
from datetime import datetime, timedelta


def get_current_user():
    # Change impelementation to get the verified user
    return User.query.all()[0]

@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()

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


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    if refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()
    return None

@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    current_tokens = Token.query.filter_by(
        client_id=request.client.client_id, user_id=request.user.id
    )
    # Every client should have only one active token, hence removing the old
    for x in current_tokens:
        x.delete()
    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token.get('access_token'),
        refresh_token=token.get('refresh_token'),
        token_type=token.get('token_type'),
        _scopes=token.get('scope'),
        expires=expires,
        client=request.client,
        user=request.user
    )
    db.session.add(tok)
    db.session.commit()
    return tok


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

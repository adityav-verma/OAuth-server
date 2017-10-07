from app import db
import uuid

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def check_password(self, password):
        return self.password == password

    def __repr__(self):
        return '<User id: {}, name: {}>'.format(self.id, self.name)


# OAuth related models

class Client(db.Model):
    name = db.Column(db.String(50), nullable=False)
    client_id = db.Column(
        db.String(100), default=uuid.uuid4, primary_key=True
    )
    client_secret = db.Column(
        db.String(50), nullable=False, index=True, unique=True
    )
    _is_confidential = db.Column(db.Boolean, nullable=False)
    _allowed_grant_types = db.Column(db.Text, nullable=False)
    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split(' ')
        return []

    @property
    def _default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split(' ')
        return []

    @property
    def client_type(self):
        return 'confidential' if self._is_confidential else 'public'

    @property
    def default_redirect_uri(self):
        if self.redirect_uris:
            return self.redirect_uris[0]
        else:
            return None

    @property
    def allowed_grant_types(self):
        if self._allowed_grant_types:
            return self._allowed_grant_types.split(' ')
        return []

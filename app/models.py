from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def check_password(self, password):
        return self.password == password

    def __repr__(self):
        return '<User id: {}, name: {}>'.format(self.id, self.name)
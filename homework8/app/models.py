from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

db = SQLAlchemy()


def lower(field):
    return func.lower(field)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.Text)
    pw_hash = db.Column(db.Text)

    def __init__(self, username, email, pw_hash):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash

    def __str__(self):
        return '<User %s>' % self.username


if __name__ == '__main__':
    engine = db.create_engine('postgresql://postgres:2367@localhost:5432/postgres')
    db.Model.metadata.create_all(engine)

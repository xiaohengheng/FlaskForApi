
from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm, Float, DECIMAL
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.libs.enums import Scope_dict
from app.models.base import Base, db, MixinJSONSerializer
import datetime


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))

    def keys(self):
        return ['id', 'email', 'nickname']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(form):
        with db.auto_commit():
            user = User()
            user.nickname = form.nickname.data
            user.email = form.account.data
            user.password = form.secret.data
            db.session.add(user)

    @staticmethod
    def verify_by_email(email, password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = Scope_dict[user.auth]
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)


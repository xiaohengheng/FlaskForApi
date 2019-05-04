from wtforms import StringField, IntegerField, PasswordField, FloatField
from wtforms.validators import DataRequired, length, Email, Regexp, NumberRange, EqualTo
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form


class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class UserSecureForm(Form):
    old_password = PasswordField(validators=[DataRequired()])
    new_password1 = PasswordField(validators=[
        DataRequired(), length(4, 32, message='密码长度至少需要在4到32个字符之间'),
        EqualTo('new_password2', message='两次输入的密码不一致')])
    new_password2 = PasswordField(validators=[DataRequired()])

    def __init__(self, g):
        super(UserSecureForm, self).__init__()
        self.uid = g.user.uid

    def validate_old_password(self, field):
        user = User.query.filter_by(id=self.uid).first()
        if not user.check_password(field.data):
            raise ValidationError('旧密码输入错误')


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])






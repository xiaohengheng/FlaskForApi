from flask import jsonify, g
from app.libs.tools import conditions
from app.libs.error_code import DeleteSuccess, AuthFailed, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User
from app.validators.User import UserSecureForm

api = Redprint('user')


@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_get_user(uid):
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


# 管理员 停用用户 软删除
@api.route('/<int:uid>', methods=['DELETE'])
def super_delete_user(uid):
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


#修改密码
@api.route('/secure', methods=['POST'])
@auth.login_required
def change_password():
    form = UserSecureForm(g).validate_for_api()

    with db.auto_commit():
        user = User.query.filter_by(id=g.user.uid).first()
        user.password = form.new_password1.data

    return Success()


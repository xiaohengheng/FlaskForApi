from enum import Enum


class ClientTypeEnum(Enum):     # 不同客户端登陆方式
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201


Scope_dict = {
    1: 'AdminScope',
    2: 'UserScope',
}



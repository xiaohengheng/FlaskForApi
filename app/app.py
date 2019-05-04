from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from decimal import Decimal
from app.libs.error_code import ServerError
from datetime import date


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if hasattr(o, '__dict__'):
            return o.__dict__
        if isinstance(o, Decimal):
            return str(o.quantize(Decimal('0.00')))
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder




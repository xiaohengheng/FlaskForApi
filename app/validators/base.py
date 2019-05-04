from flask import request
from wtforms import Form, IntegerField
from wtforms.validators import NumberRange
from wtforms.compat import iteritems
from app.libs.error_code import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # form errors
            raise ParameterException(msg=self.errors)
        return self

    # @property
    # def errors(self):
    #     # if self._errors is None:
    #     #     self._errors = dict((name, f.errors) for name, f in iteritems(self._fields) if f.errors)
    #     _form_errors = []
    #     if self._errors is None:
    #         for name, f in iteritems(self._fields):
    #             if f.errors:
    #                 for item in f.errors:
    #                     _form_errors.append(item)
    #         #self._errors = list((f.errors) for name, f in iteritems(self._fields) if f.errors)
    #     return _form_errors




class SearchForm(BaseForm):
    limit = IntegerField(validators=[NumberRange(min=1, max=100)], default=10)
    page = IntegerField(validators=[NumberRange(min=1)], default=1)


class DelForm(BaseForm):
    id = IntegerField()




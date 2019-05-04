from decimal import Decimal


def conditions(form):
    conditions = {}
    pop_keys = ['page', 'limit', 'id', 'start', 'end']
    if hasattr(form, 'pop_fields'):
        pop_keys += form.pop_fields
    for key, value in form.data.items():
        if key not in pop_keys and value != '' and value is not None:
            conditions[key] = value
    return conditions



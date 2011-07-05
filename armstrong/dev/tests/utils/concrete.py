from django.db import connection
from django.core.management.color import no_style
import random

def create_concrete_table(func=None, model=None):
    style = no_style()
    seen_models = connection.introspection.installed_models(
            connection.introspection.table_names())

    def actual_create(model):
        sql, _references = connection.creation.sql_create_model(model, style,
                seen_models)
        cursor = connection.cursor()
        for statement in sql:
            cursor.execute(statement)

    if func:
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            actual_create(self.model)
        return inner
    elif model:
        actual_create(model)


def destroy_concrete_table(func=None, model=None):
    style = no_style()
    # Assume that there are no references to destroy, these are supposed to be
    # simple models
    references = {}

    def actual_destroy(model):
        sql = connection.creation.sql_destroy_model(model, references, style)
        cursor = connection.cursor()
        for statement in sql:
            cursor.execute(statement)

    if func:
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            actual_destroy(self.model)
        return inner
    elif model:
        actual_destroy(model)


# TODO: pull into a common dev package so all armstrong code can use it
def concrete(klass):
    attrs = {'__module__': concrete.__module__, }
    while True:
        num = random.randint(1, 10000)
        if num not in concrete.already_used:
            break
    return type("Concrete%s%d" % (klass.__name__, num), (klass, ), attrs)
concrete.already_used = []

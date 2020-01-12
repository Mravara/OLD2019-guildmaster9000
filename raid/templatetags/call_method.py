from django import template

register = template.Library()

@register.simple_tag
def call_method(obj, method_name, *args):
    print(obj)
    print(method_name)
    print(args)
    method = getattr(obj, method_name)
    return method(*args)
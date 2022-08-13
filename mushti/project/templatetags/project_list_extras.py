from django import template


register = template.Library()

@register.filter
def formatdesc(value):
    """Removes all values of arg from the given string"""
    if len(value) > 100:
        last_index = value.rfind(" ", 0, 100)
        new_value = value[0:last_index] + '.....'
    else:
        new_value = value

    return new_value


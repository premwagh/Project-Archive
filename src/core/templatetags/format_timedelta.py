from datetime import timedelta as timedelta_class
from django import template


register = template.Library()

@register.filter
def timedelta(value, arg=''):
    second = None
    if isinstance(value, int):
        second = value
    elif isinstance(value, str):
        try:
            second = int(value)
        except Exception:
            pass
    elif isinstance(value, timedelta_class):
        second = value.total_second()
    if second:
        magnitudes = {}
        magnitudes['day'], rem = divmod(second, 86400)
        magnitudes['hour'], rem = divmod(rem, 3600)
        magnitudes['minute'], rem = divmod(rem, 60)
        magnitudes['second'] = rem
        magnitudes_str = [
            f"{int(v)} {k}{'s' if int(v)>1 else ''}"
            for k, v in magnitudes.items() if v
        ]
        if arg and arg == 'use_and' and len(magnitudes_str)>1:
            delta_str = ", ".join(magnitudes_str[:-1])
            delta_str = " and ".join([delta_str]+magnitudes_str[-1:])
        else:
            delta_str = ", ".join(magnitudes_str)
        return delta_str
    return ''
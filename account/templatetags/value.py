from django import template

register = template.Library()


@register.filter(name='from_ex_false')
def from_ex_false(request):
    request.session['from_ex'] = False
    return ''



register.filter('from_ex_false', from_ex_false)
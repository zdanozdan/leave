from django import template

register = template.Library()

@register.filter
def getByKey ( item, string ):
    return item.get(string,'')

@register.filter
def flatit(string,arg=" "):
    return arg.join(string)



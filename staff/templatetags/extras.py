from django import template

register = template.Library()

@register.filter(name = "space_to_us")
def space_to_us(full_name):

    return full_name.replace(" ", "_")


@register.filter(name = "us_to_space")
def us_to_space(full_name):

    return full_name.replace("_", " ")

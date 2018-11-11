from django import template

register = template.Library()


@register.filter
def add_class(form_widget, css_class):
	""" Adds a css class to a django form widget """
	return form_widget.as_widget(attrs={'class': css_class})
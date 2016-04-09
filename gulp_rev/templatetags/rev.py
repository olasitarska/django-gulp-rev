from django import template
import gulp_rev

register = template.Library()


register.simple_tag(gulp_rev.static_rev, name='static_rev')

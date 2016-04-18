import os
import json

from django.conf import settings
from django.templatetags.static import StaticNode
from django.utils.crypto import get_random_string


_STATIC_MAPPING = None


def is_debug():
    return getattr(settings, 'DEBUG', False)

def _get_mapping():
    """
    Finds and loads gulp's rev-manifest.json file.
    In default, this is looking for rev-manifest.json file places in your
    STATIC_ROOT. Can be overriden to a specific location by setting
    DJANGO_GULP_REV_PATH.
    """
    global _STATIC_MAPPING

    if _STATIC_MAPPING is None:
        manifest_path = getattr(settings,
            'DJANGO_GULP_REV_PATH',
            os.path.join(getattr(settings, 'STATIC_ROOT', ''), 'rev-manifest.json'))
        
        try:
            with open(manifest_path) as manifest_file:
                _STATIC_MAPPING = json.load(manifest_file)
        except IOError:
            return None

    return _STATIC_MAPPING

def dev_url(original):
    """
    For a dev envioronment (DEBUG=True), appends 8 random characters at the
    end of original path created by Django's {% static %} template tag.
    """
    return "{}?{}".format(original, get_random_string(length=8))

def production_url(path, original):
    """
    For a production environment (DEBUG=False), replaces original path
    created by Django's {% static %} template tag with relevant path from
    our mapping.
    """
    mapping = _get_mapping()
    if mapping:
        if path in mapping:
            return original.replace(path, mapping[path])
        return original
    else:
        return dev_url(original)

def static_rev(path):
    """
    Gets a joined path with the STATIC_URL setting, and applies revisioning
    depending on DEBUG setting.

    Usage::
        {% load rev %}
        {% static_rev "css/base.css" %}

    Example::
        {% static_rev "css/base.css" %}
        On DEBUG=True will return: /static/css/base.css?d9wdjs
        On DEBUG=False will return: /static/css/base-d9wdjs.css
    """
    static_path = StaticNode.handle_simple(path)

    if is_debug():
        return dev_url(static_path)

    return production_url(path, static_path)

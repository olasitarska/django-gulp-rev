#!/bin/bash
export DJANGO_SETTINGS_MODULE=test_app.settings
export PYTHONPATH=$PYTHONPATH:.
django-admin test
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}
USE_TZ = False
SITE_ID = 1
SECRET_KEY = '{{secret_key}}'

ROOT_URLCONF = 'test_app.urls'
STATIC_URL = '/static/'
STATIC_ROOT = ''

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gulp_rev',
    'test_app',
)

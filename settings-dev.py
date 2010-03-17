# Django settings for caquitv project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEVELOPMENT = True
if DEVELOPMENT: 
    import sys
    sys.path.append('/home/paco/Dropbox/Programas/caquitv')
    sys.path.append('/home/paco/Dropbox/Programas/caquitv/external_apps')
    sys.path.append('/home/paco/Dropbox/Programas/caquitv/local_apps')

BASE_URL=''

import os.path
PROJECT_DIR = os.path.dirname(__file__)

ADMINS = (
    ('Paco', 'psalido@gmail.com'),
)

MANAGERS = ADMINS

#DEVELOPMENT:
DATABASE_ENGINE = 'sqlite3'           
DATABASE_NAME = 'caquitv.db'            
DATABASE_USER = ''             
DATABASE_PASSWORD = ''         
DATABASE_HOST = ''             
DATABASE_PORT = ''             

     
TIME_ZONE = 'Europe/Madrid'

LANGUAGE_CODE = 'es-es'

ugettext = lambda s: s

LANGUAGES = (
    ('en', ugettext('English')),  
    ('es', ugettext('Spanish')),
)

SITE_ID = 1

USE_I18N = True
I18N_URLS = False

#MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
<<<<<<< HEAD:settings.py
MEDIA_ROOT = '//home/paco/Dropbox/Programas/caquitv/static/'
MEDIA_URL = 'http://localhost/media/'
=======
MEDIA_ROOT = '/home/some/path/media/'
MEDIA_URL = 'http://change.it/media/'
>>>>>>> 8f899d6eba48ff596d084a32999c347236ece3bd:settings.py

LOGIN_REDIRECT_URL = '/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = 'd%vcp!51p&tk6e__e$##zu6sq%k8ir%%2gf((no8p2ugcx4l9z'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

AUTH_PROFILE_MODULE = 'accounts.userprofile'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media"
    )


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'caquitv.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.formtools',
    'django.contrib.comments',
    'tvshow',
    'accounts',
    'registration',
    'profiles',
    'djangoratings',
    'chronograph',
)

ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_HOST=''
EMAIL_PORT=587
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[Caqui.tv] '

RATINGS_VOTES_PER_IP = 3

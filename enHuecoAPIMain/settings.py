"""
Django settings for enHuecoAPI project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


TEMPLATE_DIRS = (
#    BASE_DIR+ '/templates/',
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n!m-67abfo)96p4-#caj1n4%bsyzsll!(kjs2gmijh4z+6*sdt'


PRODUCTION = False
if 'acm' in socket.gethostname():
    PRODUCTION = True

DEBUG = not PRODUCTION
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['acm.uniandes.edu.co']



# CORS

CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = (

#    'django.contrib.admin',
#    'django.contrib.auth',
#    'django.contrib.contenttypes',
#    'django.contrib.sessions',
#    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
    'authentication',
    'tokenizer',
    'core',
    'schedules',
    'corsheaders',
    'rest_framework_swagger'

)

MIDDLEWARE_CLASSES = (

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.security.SecurityMiddleware'


)

ROOT_URLCONF = 'enHuecoAPIMain.urls'

WSGI_APPLICATION = 'enHuecoAPIMain.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

#USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# MODEL CONSTANTS

USER_MODEL = 'users.User'
TOKENIZER_MODEL = 'tokenizer.Tokenizer'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# ./manage.py collectstatic
# chmod 664 ~/enhueco/db.sqlite3
# sudo chown :www-data ~/enhueco/db.sqlite3
# sudo chown :www-data ~/enhueco



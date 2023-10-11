from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-^6zd(_j43e=7s91xq$6te$7qok&kh2l8yg5j71+zi*=#tzr@sx'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party
    'crispy_forms',
    "crispy_bootstrap5",
    'markdown_deux',
    'pagedown', 

    # own
    'apps.accounts.apps.UsersConfig',
    'apps.comments',
    'apps.posts',
    'apps.store',
    'apps.landing',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MARKDOWN_DEUX_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.codehilite",
    "markdown.extensions.toc",
    "markdown.extensions.tables",
    "markdown.extensions.headerid",  # Add this line for heading IDs
]

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
            # Add any other Markdown extensions you want to enable.
        },
        "safe_mode": "escape",
    },
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Place this before AuthenticationMiddleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Include your template directory path here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # or 'cache' for caching sessions
SESSION_COOKIE_NAME = 'non_auth_cookie_583'  # Replace with your chosen name


LOGIN_URL= '/login/'
LOGIN_REDIRECT_URL= '/'

ROOT_URLCONF = 'core.urls'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")


MEDIA_ROOT = os.path.join(BASE_DIR,"media_cdn")
MEDIA_URL = "/media/"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

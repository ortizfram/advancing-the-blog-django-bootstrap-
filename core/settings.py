from pathlib import Path
import os
import dotenv

dotenv.load_dotenv()

SECRET_KEY =  os.getenv('SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent

TIME_ZONE = 'America/Buenos_Aires'

DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.CustomUser'

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
    'django_social_share', 

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


#SMTP Configuration
# email settings for built-in password reset function
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  #tls
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')#google app_name after 2step verification


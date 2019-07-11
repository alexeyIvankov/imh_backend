import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'imhcorpdb',
        'USER': 'ivankov',
        'PASSWORD': '8271935',
        'HOST': 'postgresql',
        'PORT': '5432',
    }
}

HOST_URL = 'https://corp-app.metholding.com/'

SOCIAL_NETWORK= {

    'yammer':{
        'redirect_url': 'social-network/yammer/redirecturl.com',
        'client_secret': 'G18h7lLrYHZGC3adXkD1VReCq9eihBaZ5r8wtKtHsms',
        'client_id': 'gjPqfCJEGBuRl6K4Hw79g',
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/logs/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['file', 'console'],
            'propagate': True,
         },
    },
}
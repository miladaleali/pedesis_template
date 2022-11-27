# look for Settings and LazySettings in link below.
# https://github.com/django/django/blob/13a9cde133ac82e33dd091ca9bb9c677804afbe1/django/conf/__init__.py#L180
import os
from pathlib import Path
from pedesis.conf.global_settings import BaseStationSettings

from pedesis.cache.models import CacheSetting
from pedesis.db.models import DataBaseSetting

BASE_DIR = Path(__file__).resolve().parent.parent
STATION_NAME = __file__.split('/')[-2]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f409b303dbd1c051d901002cdf0c008f3d2860da91c3d9db13039683fefe2bd2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_BROKERS = [
    'pedesis.components.broker.templates.okx',
]

INSTALLED_DATA_SOURCES = {
    'okx': 'pedesis.components.broker.templates.okx',
}

INSTALLED_CACHES = {
    'main': CacheSetting(
        controller='pedesis.cache.controller.CacheHandler',
        host=os.environ.get('REDIS_HOST', 'localhost'),
        port=6379,
        db=1
    ),
    'async': CacheSetting(
        controller='pedesis.cache.controller.AsyncCacheHandler',
        host=os.environ.get('REDIS_HOST', 'localhost'),
        port=6379,
        db=1
    )
}

INSTALLED_DATABASES = {
    'default': DataBaseSetting(
        controller='pedesis.db.controller.LiveDataBase',
        url=os.environ['DATABASE_URL'],
    ),
}

# when server start, it will import all engines to it. 
# NOTE below add all engines name in this list, and parent dir is where manage.py is located.
INSTALLED_ENGINES = [
    'scalp',
]

MIDDLEWARE = []

TIME_ZONE = 'UTC'

USE_TZ = True

class StationSettings(BaseStationSettings):
    installed_engines: list[str] = [
        'scalp',
    ]

    installed_brokers: list[str] = [
        'pedesis.components.broker.templates.okx',
    ]

    installed_data_sources: dict[str, str] = {
        'okx': 'pedesis.components.broker.templates.okx',
    }

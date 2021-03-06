# -*- coding: utf-8 -*-

import os
from weppy import App
from weppy.cache import Cache, RedisCache
from weppy.orm import Database
from weppy_haml import Haml
from weppy_sentry import Sentry
from redis import Redis

app = App(__name__)

app.config.static_version = '1.5.0'
app.config.static_version_urls = True
app.config.url_default_namespace = "main"
app.config_from_yaml('redis.yml', 'redis')
app.config_from_yaml('sentry.yml', 'Sentry')
app.config.Haml.set_as_default = True

app.use_extension(Haml)
app.use_extension(Sentry)

from .models import Version, Extension

db = Database(app, auto_migrate=True)
db.define_models(Version, Extension)

redis = Redis(**app.config.redis)
cache = Cache(redis=RedisCache(**app.config.redis))

app.pipeline = [db.pipe]

from .controllers import main, docs, extensions
from . import commands

#: ensure 'docs' folder presence
if not os.path.exists(os.path.join(app.root_path, "docs")):
    os.mkdir(os.path.join(app.root_path, "docs"))

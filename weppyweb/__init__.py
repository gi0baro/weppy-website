import os
from weppy import App, Cache, DAL, sdict
from redis import Redis


## init our app
app = App(__name__)
app.config.static_version = '1.1.0'
app.config.static_version_urls = True
app.config.url_default_namespace = "main"
app.config.redis = sdict(
    host="localhost",
    port=6379,
    db=1
)

from weppy_haml import Haml
app.config.Haml.set_as_default = True
app.use_extension(Haml)

from models import Version, Extension
db = DAL(app)
db.define_models([Version, Extension])

redis = Redis(host=app.config.redis.host, port=app.config.redis.port,
              db=app.config.redis.db)

cache = Cache()

app.expose.common_handlers = [db.handler]

from controllers import main, docs, extensions

import commands

#: ensure 'docs' folder presence
if not os.path.exists(os.path.join(app.root_path, "docs")):
    os.mkdir(os.path.join(app.root_path, "docs"))

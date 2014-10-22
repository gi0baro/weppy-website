from weppy import App, Cache


## init our app
app = App(__name__)
app.config.static_version = '1.0.0'
app.config.static_version_urls = True
app.config.url_default_namespace = "main"

from weppy_haml import Haml
app.config.Haml.set_as_default = True
app.use_extension(Haml)

cache = Cache()

from controllers import main, docs

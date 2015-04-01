from weppy import AppModule, abort
from weppyweb import app, db


ext = AppModule(app, "ext", __name__, url_prefix="extensions",
                template_folder="ext")


@ext.expose("/")
def index():
    extensions = db(db.Extension.id > 0).select(orderby=~db.Extension.updated)
    return dict(extensions=extensions)


@ext.expose("/<str:ename>")
def detail(ename):
    extension = db(db.Extension.slug == ename).select().first()
    if not extension:
        abort(404)
    return dict(extension=extension)

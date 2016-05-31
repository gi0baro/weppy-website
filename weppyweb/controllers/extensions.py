from markdown2 import markdown
from weppy import AppModule, abort, asis
from weppyweb import app, db, cache


ext = AppModule(app, "ext", __name__, url_prefix="extensions",
                template_folder="ext")


@ext.route("/")
def index():
    extensions = db(db.Extension.id > 0).select(orderby=~db.Extension.updated)
    return dict(extensions=extensions)


def build_html(name, md):
    def _parse():
        extras = ['tables', 'fenced-code-blocks', 'header-ids']
        return markdown(md, extras=extras).encode('utf-8')
    return cache('ext_'+name+'_html', _parse, 300)


@ext.route("/<str:ename>")
def detail(ename):
    extension = db(db.Extension.slug == ename).select().first()
    if not extension:
        abort(404)
    html = build_html(extension.name, extension.data)
    return dict(extension=extension, body=asis(html))

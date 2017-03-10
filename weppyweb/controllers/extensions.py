# -*- coding: utf-8 -*-

from markdown2 import markdown
from weppy import abort, asis
from weppyweb import app, db, cache, Extension


ext = app.module(
    __name__, "ext", url_prefix="extensions", template_folder="ext")


@ext.route("/")
def index():
    extensions = Extension.all().select(orderby=~Extension.updated)
    return dict(extensions=extensions)


def build_html(name, md):
    def _parse():
        extras = ['tables', 'fenced-code-blocks', 'header-ids']
        return markdown(md, extras=extras).encode('utf-8')
    return cache('ext_' + name + '_html', _parse, 300)


@ext.route("/<str:ename>")
def detail(ename):
    extension = db(Extension.slug == ename).select().first()
    if not extension:
        abort(404)
    html = build_html(extension.name, extension.data)
    return dict(extension=extension, body=asis(html))

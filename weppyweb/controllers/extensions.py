# -*- coding: utf-8 -*-

from markdown2 import markdown
from weppy import abort, asis
from weppy.validators.process import Urlify
from .. import app, db, cache, Extension


ext = app.module(
    __name__, "ext", url_prefix="extensions", template_folder="ext")


@ext.route("/")
@cache.response(query_params=False, language=False, duration=600)
def index():
    extensions = Extension.all().select(orderby=~Extension.updated)
    return dict(extensions=extensions)


@ext.route("/<str:ename>")
@cache.response(query_params=False, language=False, duration=600)
def detail(ename):
    extension = db(Extension.slug == ename).select().first()
    if not extension:
        abort(404)
    html = markdown(
        extension.data,
        extras=['tables', 'fenced-code-blocks', 'header-ids']
    ).encode('utf-8')
    _sections = _get_sections(extension.data)
    sections = []
    for s in _sections:
        sections.append((s, Urlify(keep_underscores=True)(s)[0]))
    return dict(extension=extension, body=asis(html), sections=sections)


def _get_sections(text):
    sections = []
    lines = text.split('\n')
    for _, line in enumerate(lines):
        if line.startswith("---"):
            sections.append(lines[_ - 1].replace("\\", ""))
        elif line.startswith("## "):
            sections.append(line[3:].replace("\\", ""))
    return sections

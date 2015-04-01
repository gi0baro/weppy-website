import os
from yaml import load as ymlload
from markdown2 import markdown
from weppyweb import app, cache

_docs_path = os.path.join(app.root_path, 'docs')


def get_versions():
    def _get():
        versions = []
        for name in os.listdir(_docs_path):
            if name != "dev" and os.path.isdir(os.path.join(_docs_path, name)):
                versions.append(name)
        return sorted(versions, reverse=True)
    return cache('docs_versions', _get, 600)


def get_latest_version():
    latest_version = max([float(v) for v in get_versions()])
    return str(latest_version)


def is_page(version, name):
    path = os.path.join(_docs_path, version, name+".md")
    if os.path.exists(path):
        return True
    return False


def _get_lines(version, name):
    path = os.path.join(_docs_path, version, name+".md")
    with open(path) as f:
        lines = f.readlines()
    return lines


def _get_chapter(version, name):
    def _get():
        lines = _get_lines(version, name)
        chapter = name
        for i in range(0, len(lines)):
            if lines[i].startswith("==="):
                chapter = lines[i-1]
                break
        return chapter
    return cache('docs_'+version+'_'+name+'_chapter', _get, 300)


def get_sections(version, name):
    def _get():
        lines = _get_lines(version, name)
        sections = []
        for i in range(0, len(lines)):
            if lines[i].startswith("---"):
                sections.append(lines[i-1])
        return sections
    return cache('docs_'+version+'_'+name+'_sections', _get, 300)


def build_tree(version):
    def _get():
        with open(os.path.join(folder, 'tree.yml')) as f:
            tree = ymlload(f)
        complete_tree = []
        for name in tree:
            ch_name = _get_chapter(version, name)
            sub_tree = get_sections(version, name)
            complete_tree.append((ch_name, name, sub_tree))
        return complete_tree

    folder = os.path.join(_docs_path, version)
    if not os.path.exists(folder):
        return None
    return cache('docs_'+version+'_tree', _get, 300)


def get_text(version, name):
    fpath = os.path.join(_docs_path, version, name+".md")
    if not os.path.exists(fpath):
        return None
    with open(fpath) as f:
        text = f.read()
    return text


def get_html(version, name):
    def _parse():
        extras = ['tables', 'fenced-code-blocks', 'header-ids']
        return markdown(text, extras=extras).encode('utf-8')

    text = get_text(version, name)
    if text is None:
        return text
    return cache('docs_'+version+'_'+name+'_html', _parse, 300)

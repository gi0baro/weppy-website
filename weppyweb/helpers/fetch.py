import requests
import os
import shutil
from subprocess import Popen, PIPE
from yaml import load as ymlload
from weppy.validators import Slug
from weppyweb import app, redis, db


class GitGetter(object):
    def __init__(self, repo, store_in):
        self.repo = repo
        self.tfolder = os.path.join(app.root_path, "tmp")
        self.storage = store_in
        self._empty = False
        if not os.path.exists(self.tfolder):
            os.mkdir(self.tfolder)
        if not os.path.exists(self.folder):
            self._empty = True

    @property
    def folder(self):
        return os.path.join(self.tfolder, self.storage)

    def _clone(self):
        os.chdir(self.tfolder)
        Popen(['git', 'clone', self.repo, self.storage]).wait()

    def get(self):
        if self._empty:
            self._clone()
            return
        os.chdir(self.folder)
        Popen(['git', 'pull']).wait()

    def tags(self):
        os.chdir(self.folder)
        return set(
            Popen(['git', 'tag'], stdout=PIPE).communicate()[0].splitlines())


class Getter(object):
    def __init__(self):
        self.tfolder = os.path.join(app.root_path, "temp")
        if not os.path.exists(self.tfolder):
            os.mkdir(self.tfolder)

    def get(self, url):
        try:
            r = requests.get(url, timeout=15)
            assert r.status_code == 200
            self.data = r.text
        except:
            app.log.debug("GETTER: Error requesting "+url)
            self.data = None

    def download(self, url, fname=None):
        if not fname:
            fname = url.split("/")[-1]
        fname = os.path.join(self.tfolder, fname)
        r = requests.get(url, timeout=15, stream=True)
        if r.status_code == 200:
            with open(fname, "wb") as f:
                app.log.debug("GETTER: downloading file from url: "+url+"...")
                for chunk in r.iter_content():
                    f.write(chunk)
            app.log.debug("GETTER: download completed.")
            return fname
        return None


def _update_version():
    f = open(os.path.join(app.root_path, "tmp", "weppysrc", "CHANGES"), "r")
    lines = f.readlines()
    f.close()
    for i in range(0, len(lines)):
        if lines[i].startswith("---"):
            if lines[i-1].startswith("Version"):
                n = lines[i-1].split("Version ")[1]
                codename = lines[i+2].split(", codename ")[1]
                break
    redis.set("weppy:last_version", n+" "+codename)


def _update_docs(tags):
    versions = {}
    for tag in tags:
        split = tag[1:].split(".")
        sub = split[0]+"."+split[1]
        if not versions.get(sub):
            versions[sub] = tag[1:]
        else:
            if float(tag[3:]) > float(versions[sub][2:]):
                versions[sub] = tag[1:]
    db._adapter.reconnect()
    upd_list = []
    for k, v in versions.items():
        row = db.Version(name=k)
        if not row:
            upd_list.append((k, v))
            db.Version.insert(name=k, gittag=v)
        elif row.gittag != v:
            upd_list.append((k, v))
            row.update_record(gittag=v)
    db.commit()
    #: update versioned docs (if needed)
    for k, v in upd_list:
        docs_path = os.path.join(app.root_path, "docs", k)
        if not os.path.exists(docs_path):
            os.mkdir(docs_path)
        os.chdir(os.path.join(app.root_path, "tmp", "weppysrc"))
        Popen(["git", "checkout", "v"+v]).wait()
        src_path = os.path.join(app.root_path, "tmp", "weppysrc", "docs")
        for name in os.listdir(src_path):
            shutil.copy2(os.path.join(src_path, name), docs_path)
    #: update 'dev' docs
    docs_path = os.path.join(app.root_path, "docs", "dev")
    if not os.path.exists(docs_path):
        os.mkdir(docs_path)
    os.chdir(os.path.join(app.root_path, "tmp", "weppysrc"))
    Popen(["git", "checkout", "master"]).wait()
    src_path = os.path.join(app.root_path, "tmp", "weppysrc", "docs")
    for name in os.listdir(src_path):
        shutil.copy2(os.path.join(src_path, name), docs_path)


def update_base():
    getter = GitGetter("https://github.com/gi0baro/weppy.git", "weppysrc")
    getter.get()
    _update_version()
    _update_docs(getter.tags())


def _update_extensions():
    os.chdir(os.path.join(app.root_path, "tmp", "registry"))
    Popen(["git", "checkout", "stable"]).wait()
    db._adapter.reconnect()
    src_path = os.path.join(app.root_path, "tmp", "registry", "extensions")
    for name in os.listdir(src_path):
        statusfile = open(os.path.join(src_path, name, 'status.yml'), 'r')
        statusdata = ymlload(statusfile)
        statusfile.close()
        if statusdata['approved']:
            status = statusdata['status']
            metafile = open(os.path.join(src_path, name, 'data.yml'), 'r')
            metadata = ymlload(metafile)
            metafile.close()
            datafile = open(os.path.join(src_path, name, 'page.md'), 'r')
            extdata = datafile.read()
            datafile.close()
            row = db.Extension(name=metadata['name'])
            if not row:
                slug = Slug()(metadata['name'])[0]
                rid = db.Extension.insert(
                    name=metadata['name'],
                    slug=slug
                )
                row = db.Extension(id=rid)
            row.update_record(
                status=status,
                author_name=metadata['author']['name'],
                author_email=metadata['author']['email'],
                description=metadata['description'],
                github=metadata['github'],
                pypi=metadata['pypi'],
                version=metadata['version'],
                website=metadata.get('website'),
                bugtracker=metadata['bugtracker'],
                license=metadata['license'],
                data=extdata
            )
    db.commit()


def update_extensions():
    getter = GitGetter("https://github.com/gi0baro/weppyreg.git", "registry")
    getter.get()
    _update_extensions()

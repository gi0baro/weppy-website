from datetime import datetime
from weppy.dal import Model, Field


class Version(Model):
    tablename = "versions"

    fields = [
        Field("name"),
        Field("gittag")
    ]


class Extension(Model):
    tablename = "extensions"

    fields = [
        Field("name"),
        Field("slug"),
        Field("author_name"),
        Field("author_email"),
        Field("github"),
        Field("pypi"),
        Field("version"),
        Field("website"),
        Field("bugtracker"),
        Field("license"),
        Field("updated", "datetime", default=lambda: datetime.utcnow())
    ]

    updates = {
        "updated": lambda: datetime.utcnow()
    }

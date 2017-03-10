# -*- coding: utf-8 -*-

from rq import Queue, Connection, Worker
from weppyweb import app, redis
from weppyweb.helpers.scheduler import Scheduler


@app.command('scheduler')
def schedule():
    sched = Scheduler()
    sched.run()


@app.command('queue_def')
def _q_default():
    with Connection(connection=redis):
        qs = [Queue('default')]
        w = Worker(qs)
        w.work()

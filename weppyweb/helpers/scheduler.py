from datetime import datetime, timedelta
from weppyweb import redis
from .fetch import update_base, update_extensions


class Scheduler(object):
    JN = 1

    def __init__(self):
        from rq_scheduler.scheduler import Scheduler
        self.scheduler = Scheduler(connection=redis, interval=60)

    def check_jobs(self):
        now = datetime.utcnow()
        self.my_jobs = self.scheduler.get_jobs(with_times=True)
        ## check correct n of jobs
        if len(self.my_jobs) < self.JN:
            return False
        ## check expired jobs
        for j, t in self.my_jobs:
            if t <= now:
                return False
        return True

    def delete_jobs(self):
        for el in self.my_jobs:
            self.scheduler.cancel(el[0])
        self.my_jobs = []

    def create_jobs(self):
        # version and docs grab
        date = datetime.utcnow()+timedelta(seconds=15)
        job = self.scheduler.schedule(
            scheduled_time=date,
            func=update_base,
            interval=3600,
            repeat=None
        )
        self.my_jobs.append((job.id, date))
        # extensions grab
        date = datetime.utcnow()+timedelta(seconds=45)
        job = self.scheduler.schedule(
            scheduled_time=date,
            func=update_extensions,
            interval=7200,
            repeat=None
        )
        self.my_jobs.append((job.id, date))

    def run(self):
        self.check_jobs()
        self.delete_jobs()
        self.create_jobs()
        self.scheduler.run()

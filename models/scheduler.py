# -*- coding: utf-8 -*-
from gluon.scheduler import Scheduler
from zadachi import reporting_percentages,sozdanie_bazy
#web2py -K dabkrs
schedb=DAL('sqlite://schedb.sqlite')
scheduler = Scheduler(schedb)
schedb.scheduler_task.task_name.compute=lambda row: "test"

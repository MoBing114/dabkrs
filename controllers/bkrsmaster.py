# -*- coding: utf-8 -*-
import os

def index():
    return dict(
        form=SQLFORM.smartgrid(
            schedb.scheduler_run,
            csv=False, showbuttontext=False,
            advanced_search=False
        )
               )
def get_file_name(form):
    if request.vars.dictfile!=None:
        form.vars.dictfilename = request.vars.dictfile.filename

def obrabotka(file):
    pass

def slovari():
    grid = SQLFORM.grid(istochniki,
                    csv=False,
                    showbuttontext=False,
                    advanced_search=False,
                    selectable = [('Обработать',obrabotka)],
                    onvalidation=get_file_name
                   )
    return dict(grid=grid)

def tasks():
    return dict(
        form=SQLFORM.smartgrid(
            schedb.scheduler_task,
            csv=False, showbuttontext=False,
            advanced_search=False
        )
               )

def addtask():
    taskfunc=sozdanie_bazy#reporting_percentages
    task_name=taskfunc.__doc__.split("\n")[0] if taskfunc.__doc__!=None else taskfunc.__name__
    scheduler.queue_task(taskfunc,
                         task_name=task_name,
                         pvars=dict(file="static/dsl/dabkrs_160922.dsl",truncate=True),
                         timeout=10800,
                         sync_output=3)
    return redirect(URL('tasks'))
def indexing():
    db.executesql('CREATE INDEX IF NOT EXISTS slovoidx ON slovar (slovo);')
    db.executesql('CREATE INDEX IF NOT EXISTS pinyinidx ON slovar (pinyin);')
    db.executesql('CREATE INDEX IF NOT EXISTS perevodidx ON slovar (perevod);')
    return "Индексация выполнена"

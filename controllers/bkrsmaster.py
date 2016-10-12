# -*- coding: utf-8 -*-
import os
import sys
def index():
    return dict()

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
    response.view='bkrsmaster/grid.load'
    return dict(
        grid=SQLFORM.grid(
            schedb.scheduler_task,
            csv=False, showbuttontext=False,
            advanced_search=False,
            searchable=False,
            create=False,
        )
    )
def runs():
    #schedb.scheduler_run.run_output.represent=lambda value,row:DIV(DIV(value,
                                                                       #_class="progress-bar",
                                                                       #aria=dict(valuenow=value,valuemin="0",valuemax="9"),
                                                                       #_style="width: {0:.0%};".format(int(value if value!=None else 0)/9.0)),
                                                                   #_class="progress progress-striped active")
    response.view='bkrsmaster/grid.load'
    return dict(
        grid=SQLFORM.grid(
            schedb.scheduler_run,
            csv=False, showbuttontext=False,
            advanced_search=False,
            searchable=False,
            create=False,
        )
    )
def worker_buttons(row):
    acticons=[
       ['activate',"glyphicon glyphicon-ok-circle","btn btn-success","Задействовать"],
       ['disable',"glyphicon glyphicon-off","btn btn-primary","На отдых по завершении задачи"],
       ['stop_task',"glyphicon glyphicon-stop","btn btn-danger","Остановить задачу немедленно"],
       ['terminate',"glyphicon glyphicon-remove-sign","btn btn-warning","Убить по завершении задчи"],
       ['kill',"glyphicon glyphicon-ban-circle","btn btn-danger","Убить немедленно"],
       ['pick',"glyphicon glyphicon-asterisk","btn btn-info","Писк"],
    ]
    btngrp=DIV(_class="btn-group",_role="group")
    [btngrp.append(
            TAG.button(I(_class=icon),
               _type="button",
               _class=btnclass,
               _onclick="ajax('"+URL(c='bkrsmaster', f='worker_acts',vars=dict(id=row.id,act=action))+"')",
              data=dict(toggle="tooltip"),
              _title=title
              )
        ) for action,icon,btnclass,title in acticons]
    return DIV(btngrp,_class='btn-toolbar',_role='toolbar')

def workers():
    #schedb.scheduler_worker.worker_stats.represent=lambda value,row:DIV(value,_style="width:10%;")
    response.view='bkrsmaster/grid.load'
    return dict(
        grid=SQLFORM.grid(
            schedb.scheduler_worker,
            csv=False, showbuttontext=False,
            advanced_search=False,
            searchable=False, deletable=False, editable=False, details=False, create=False,
            links=[dict(header='',body=worker_buttons)],
            links_placement = 'left'
        )
    )

def worker_acts():
    id=request.vars['id']
    action=request.vars['act']
    if action=='disable':
        schedb.scheduler_worker[id].update_record(status='DISABLED')
    elif action=='activate':
        schedb.scheduler_worker[id].update_record(status='ACTIVE')
    elif action=='kill':
        schedb.scheduler_worker[id].update_record(status='KILL')
    elif action=='terminate':
        schedb.scheduler_worker[id].update_record(status='TERMINATE')
    elif action=='stop_task':
        schedb.scheduler_worker[id].update_record(status='STOP_TASK')
    elif action=='pick':
        schedb.scheduler_worker[id].update_record(status='PICK')

def addworker():
    my_file = open(os.path.join(request.env.web2py_path,'startworker.bat'),'w')
    my_file.write('%s -K dabkrs'%('web2py.exe' if os.path.isfile(os.path.join(request.env.web2py_path,'web2py.exe')) else 'web2py.py'))
    my_file.close()
    os.startfile(os.path.join(request.env.web2py_path,'startworker.bat'))
    return "Работник запущен"

def addtask():
    
    taskfunc=sozdanie_bazy
    #taskfunc=reporting_percentages
    task_name=taskfunc.__doc__.split("\n")[0] if taskfunc.__doc__!=None else taskfunc.__name__
    scheduler.queue_task(taskfunc,
                         task_name=task_name,
                         pvars=dict(file="static/dsl/dabkrs_160928.dsl",truncate=True),
                         timeout=10800,
                         sync_output=3)
    """
    taskfunc=extract_examles#choiselist#calc_records#createlinks
    task_name=taskfunc.__doc__.split("\n")[0] if taskfunc.__doc__!=None else taskfunc.__name__
    scheduler.queue_task(taskfunc,
                         #pvars=dict(),
                         task_name=task_name,
                         timeout=10800,
                         sync_output=3)"""
    response.flash="Задача добавлена"

def indexing():
    db.executesql('CREATE INDEX IF NOT EXISTS slovoidx ON slovar (slovo);')
    db.executesql('CREATE INDEX IF NOT EXISTS pinyinidx ON slovar (pinyin);')
    db.executesql('CREATE INDEX IF NOT EXISTS perevodidx ON slovar (perevod);')
    return "Индексация выполнена"

def start_worker():
    import subprocess
    winwworker=os.path.join(request.env.web2py_path,'web2py.exe')
    pyworker=os.path.join(request.env.web2py_path,'web2py.py')
    if os.path.isfile(winwworker):
        p = subprocess.Popen([winwworker, '-K', request.application])
    else:
        p = subprocess.Popen(['python',pyworker, '-K', request.application])
    if p.poll()==None:response.flash="Работник запущен"

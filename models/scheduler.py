# -*- coding: utf-8 -*-
from gluon.scheduler import Scheduler
from zadachi import *#Импортируем все здесь, чтобы в других местах просто ссылаться по имени
import os
#web2py -K dabkrs
schedb=DAL('sqlite://schedb.sqlite')
scheduler = Scheduler(schedb)
schedb.scheduler_run.run_output.represent=lambda value,row:DIV(value,data={'id':row.id})
istochniki=schedb.define_table(
       'istochniki',
       Field('dictfile','upload',
              uploadfolder=os.path.join(request.folder,'static/dsl'),
              requires = IS_NOT_EMPTY(error_message='Файл не выбран!'),
              autodelete=True),
        Field('dictfilename',writable=False),
        Field('dicttype',
              compute=lambda row: os.path.splitext(row.dictfile)[1]),
        Field('dictsize','integer',
              compute=lambda row: os.path.getsize(os.path.join(request.folder,'static/dsl',row.dictfile))),
        Field('structura',
              requires =IS_IN_SET(['DSL', 'TSL', 'SSL'],error_message='Выберите формат структуры файла словаря'),
              comment="'DSL'-формат словарей Lingvo; 'TSL' - слова в строке, разделенные табом; 'SSL' - слова в строке, разделенные двойным пробелом"
             ),
        Field('processed','boolean', default=False, writable=False),
        format='%(dictfilename)s'
        )
istochniki.dictsize.represent=lambda value,row: str(round(value/1024.0,1))+" кБ" if value/(1024*1024.0)<1 else str(round(value/(1024*1024.0),1))+" МБ"

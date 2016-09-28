# -*- coding: utf-8 -*-
from bkrstools import repres_perevod,sokr_perevod,reshala
from gluon import current#Локальный объект потока исполнения запроса (используется в модулях)

slovar = db.define_table('slovar',
    Field('slovo','string',unique=True,label="Слово"),
    Field('pinyin',label="Пиньин"),
    Field('perevod',"text",label="Перевод"),
    Field('dlina','integer',compute=lambda row:len(row.slovo if isinstance(row.slovo,unicode) else unicode(row.slovo, 'utf-8')),label="Длина"),
    Field('choiselist','list:string',label="Варианты"),
    Field('linksto','list:reference slovar',writable=False, readable=False,label="Ссылка на"),
    Field('linksfrom','list:reference slovar',writable=False, readable=False,label="Ссылка c"),
    #Field.Virtual('short',lambda row:"",label="Краткая форма"),
    auth.signature,#Поля пользователей
    Field('is_active', 'boolean',writable=False, readable=False, default=True),#для контроля версий
    #migrate=True, fake_migrate=True,#если база заполнена вне web2py, то расскомментировать, запустить просмотр базы и обратно закомментировать
    #rname="dabkrs"#если таблица в базе имеет другое реальное имя, то задать реальное имя  (для полей тоже есть rname, на случай миграции с другой БД)
)

"""slovar._enable_record_versioning(#включаем версионность
    archive_db=db,#версии храним в этойже базе
    archive_name='slovar_archive',#в архивной таблице с этим названием
    current_record='current_slovo',#с этим полем идентификатора в архивной таблице на измененную запись
    is_active='is_active',#полем для пометки об удалении в основной таблице
    current_record_label="Измененная запись"
)"""

current.db=db#Создает атрибут со ссылкой на базу данных (для ипользования в модулях)
current.slovar=slovar#Создает атрибут со ссылкой на таблицу в базе данных (для ипользования в модулях)
#Html - представления полей, используемые по умолчанию
slovar.slovo.represent=lambda slovo,row:DIV(slovo,_class="ch")#Помещаем в контейнер, чтобы применить стили оформления согласно классу
slovar.pinyin.represent=lambda pinyin,row:DIV(pinyin,_class="py")#Помещаем в контейнер, чтобы применить стили оформления согласно классу
slovar.perevod.represent=repres_perevod#Заменяем DSL-тэги на HTML-тэги, помещаем в контейнеры, чтобы применить стили оформления согласно классам
slovar.choiselist.represent=lambda value,row:UL([x for x in value])
#slovar.short.represent=lambda value,row: sokr_perevod(row.perevod,row.slovo)#Сокращенная форма перевода (убраны лишние комментарии и примеры)

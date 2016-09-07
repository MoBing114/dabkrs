# -*- coding: utf-8 -*-
from bkrstools import repres_perevod,sokr_perevod
from gluon import current#Локальный объект потока исполнения запроса (используется в модулях)
slovar = db.define_table('slovar',
                             Field('slovo','string',unique=True,label="Слово"),
                             Field('pinyin',label="Пиньин"),
                             Field('perevod',"text",label="Перевод"),
                             Field('dlina','integer',compute=lambda row:len(row.slovo),label="Длина"),
                             Field('sostav','list:reference slovar',label="Состав"),
                             Field('links','list:reference slovar',label="Ссылается"),
                             Field.Virtual('short',lambda row:"",label="Краткая форма"),
                             #migrate=True, fake_migrate=True,#если база заполнена вне web2py, то расскомментировать, запустить просмотр базы и обратно закомментировать
                             #rname="dabkrs"#если таблица в базе имеет другое реальное имя, то задать реальное имя  (для полей тоже есть rname, на случай миграции с другой БД)
                        )
current.db=db#Создает атрибут со ссылкой на базу данных (для ипользования в модулях)
current.slovar=slovar#Создает атрибут со ссылкой на таблицу в базе данных (для ипользования в модулях)
#Html - представления полей, используемые по умолчанию
slovar.slovo.represent=lambda slovo,row:DIV(slovo,_class="ch")#Помещаем в контейнер, чтобы применить стили оформления согласно классу
slovar.pinyin.represent=lambda pinyin,row:DIV(pinyin,_class="py")#Помещаем в контейнер, чтобы применить стили оформления согласно классу
slovar.perevod.represent=repres_perevod#Заменяем DSL-тэги на HTML-тэги, помещаем в контейнеры, чтобы применить стили оформления согласно классам
slovar.sostav.represent=lambda value,row: "" if value==None else DIV(*[#Контейнер со ссылками на просмотр
        A(slovar[x].slovo+", ",#Отображаемое значение
            _href='%(link)s?slovo=%(slovo)s'%dict(link=URL("slovo"), slovo=slovar[x].slovo))#Собственно ссылка
        for x in value])#Цикл по списку id ссылочных полей
slovar.links.represent=lambda value,row: "" if value==None else DIV(*[repres_perevod(slovar[x].perevod) for x in value])#Получаем html-представление всех помеченных [ref].*[/ref] слов в переводе
slovar.short.represent=lambda value,row: sokr_perevod(row.perevod,row.slovo)#Сокращенная форма перевода (убраны лишние комментарии и примеры)

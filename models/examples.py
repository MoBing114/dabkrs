# -*- coding: utf-8 -*-
examples=db.define_table('examples',
                         Field('slovo','string',unique=True,label="Слово"),
                         Field('pinyin',label="Пиньин"),
                         Field('perevod',"text",label="Перевод"),
                         Field('dlina','integer',compute=lambda row:len(row.slovo if isinstance(row.slovo,unicode) else unicode(row.slovo, 'utf-8')),label="Длина"),
                         Field('choiselist','list:string',label="Варианты"),
                         Field('sourse','list:reference slovar',label="Источник"),
                         auth.signature,#Поля пользователей
                         Field('is_active', 'boolean',writable=False, readable=False, default=True),#для контроля версий
                        )
current.examples=examples
examples.choiselist.represent=lambda value,row:UL([x for x in value])

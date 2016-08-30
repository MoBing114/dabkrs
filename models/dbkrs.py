# -*- coding: utf-8 -*-
from bkrstools import repres_perevod,create_spisok
slovar = db.define_table('slovar',
                             Field('slovo','string',unique=True,label="Слово"),
                             Field('pinyin',label="Пиньин"),
                             Field('perevod',"text",label="Перевод"),
                             Field('dlina','integer',compute=lambda row:len(row.slovo),label="Длина"),
                             Field('sostav','list:reference slovar'),
                             Field('links','list:reference slovar'),
                             Field.Virtual('spisok',lambda row:"",label="Список"),
                             migrate=True)

slovar.perevod.represent=repres_perevod
slovar.slovo.represent=lambda slovo,row:DIV(slovo,_class="ch")
slovar.pinyin.represent=lambda pinyin,row:DIV(pinyin,_class="py")
slovar.sostav.represent=lambda value,row: DIV(*[
        A(slovar[x].slovo+", ",_href='%(link)s?slovo=%(slovo)s'%dict(link=URL("slovo"), slovo=slovar[x].slovo))
                for x in value])
slovar.links.represent=lambda value,row: DIV(*[repres_perevod(slovar[x].perevod) for x in value])
slovar.spisok.represent=lambda value,row: create_spisok(row.perevod)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Данный файл(модуль) содержит функции, которые будут запускаться
в отдельном фоновом потоке (в потоке исполнения "работника").
Функции задач ставяться в очередь через метод .queue_task планировщика scheduler,
который определен в модели scheduler.py приложения web2py.
Работники запускаются вне web2py из консоли командной строки командами:
python web2py.py -K dabkrs из исходного кода(используется python версии 2.7)
или
web2py.exe -K dabkrs для исполняемого файла windows
Не забываем про документирование функций (это то что в тройных кавычках, если что),
первая строка документации будет браться как имя задачи
"""
#Оператор print почему то не записывает в поле Run Output запущеной задачи, если кодировка отличается от системной
#например если сделать импорт
#from __future__ import unicode_literals
#или выставить utf-8 по умолчанию при помощи
#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")
#то print выводить будет только на консоль, а в поле Run Output не будет.
#Для открытия файла в "utf-8" или другой кодировке, отличной от системной
#импортируем функцию с именем, аналогичным встроеной в питон
#(в питон 3.х open работает как и codecs.open, поэтому codecs не нужен)
from codecs import open
from gluon import *
import re,os,time

def reporting_percentages(*args,**vars):
    """Тестовая функция"""
    for i in range(10):
        time.sleep(5)
        print u'!clear!%d'%(i)
    return 1

def sozdanie_bazy(file,truncate=False):
    """Заполнение базы из файла словаря в формате DSL.
    Функция открывает текстовый файл словаря в формате DSL (lingvo),
    читает и разбирает по блокам при помощи регулярных выражений,
    находит "слово, пиньин и перевод" и записывает в базу данных в юникод кодировке"""
    dsl_pattern=re.compile("(?m)^\n([^ ].*?)\n (.*?)\n (.*?)$")
    if not os.path.exists(file): file=os.path.normpath(os.path.join(current.request.folder,file))
    if not os.path.exists(file): return "File not found"
    slovar=current.slovar
    db=current.db
    if truncate:slovar.truncate()
    with open(file,mode='r', encoding='utf-8') as f:
        #Общее число строк в файле для процентов
        n=len(f.readlines())
        time.sleep(5)
        f.close()
    rezult=[]
    with open(file,mode='r', encoding='utf-8') as f:
        i,j=0,0
        #файл большой, поэтому читаем его блоками по 10000 строк
        nbl=10000
        block=[unicode(f.readline())]
        while block[-1]:
            block=[block[-1]]
            [block.append(unicode(f.readline())) for ii in range(nbl)]
            i+=nbl
            #блок должен заканчиваться на строке "\n" либо на символе конца файла, проверяем и читаем дальше, пока не найдем эту строку
            while block[-1]!="\n" and block[-1]!="":
                block.append(unicode(f.readline()))
            for slovo,pinyin,perevod in dsl_pattern.findall("".join(block)):
                try:
                    slovar.insert(slovo=slovo,pinyin=pinyin,perevod=perevod)
                    j+=1
                except:
                    rezult+=u"insert error: "+slovo+u"||"+perevod
            if j%10000==0:db.commit()
            time.sleep(2)
            print u'!clear!{0:d} {1:.2%}'.format(j,float(i)/n)
        f.close()
        db.commit()
        rezult+=u"Insert comlited, added %d records"%(j)
        return u"\n".join(rezult)

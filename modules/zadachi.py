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
from gluon import *
import re,os,time,sys,chardet

def reporting_percentages(*args,**vars):
    """Тестовая функция"""
    for i in range(10):
        time.sleep(5)
        msg='!clear! готово %d'%(i)
        print msg
    return "задача выполнена"

def convertfile(filePath):
    """Пересохранение файла в кодировке "utf-8", если она отличается"""
    #Файл может быть большим, определим кодировку по первой строке
    with open(filePath, "rb") as F:
        text = F.readline()
        enc = chardet.detect(text).get("encoding")
        F.close()
    if enc and enc.lower() != "utf-8":
        #Если кодировка нужна, то открываем файл и читаем текст
        with open(filePath, "rb") as F:
            text=F.read()
            F.close()
        #Декодируем и энкодируем в нужную кодировку
        text = text.decode(enc)
        text = text.encode("utf-8")
        with open(filePath, "wb") as f:#Перезаписываем файл
            f.write(text)
            f.close()

dsl_pattern=re.compile(r"(?m)^\n([^ ].*?)\n (.*?)\n (.*?)$")

def parse_dsl(text):
    """Разборка текста в формате dsl и добавление в словарь"""
    slovar=current.slovar
    db=current.db
    inserted,updated=0,0
    for slovo,pinyin,perevod in dsl_pattern.findall(text):
        try:
            slovar.insert(
                slovo=slovo,
                pinyin=pinyin,
                perevod=perevod,
                with_examples=re.search(r"\[ex{0,1}\]",perevod)!=None
            )
            inserted+=1
        except:
            db.commit()
            row=db(slovar.slovo==slovo).select().first()
            if not row:continue
            row.perevod=perevod+row.perevod.encode('utf-8')
            row.with_examples=re.search(r"\[ex{0,1}\]",row.perevod)!=None
            row.update_record()
            updated+=1
    return inserted,updated

def sozdanie_bazy(file,truncate=False):
    """Заполнение базы из файла словаря в формате DSL.
    Функция открывает текстовый файл словаря в формате DSL (lingvo),
    читает и разбирает по блокам при помощи регулярных выражений,
    находит "слово, пиньин и перевод" и записывает в базу данных в юникод кодировке"""
    if not os.path.exists(file): file=os.path.normpath(os.path.join(current.request.folder,file))
    if not os.path.exists(file): return "Файл не найден"
    convertfile(file)#Пересохраняем в utf-8
    slovar=current.slovar
    db=current.db
    n=sum(1 for i in open(file, 'r'))#Общее число строк в файле для подсчета процентов
    with open(file,mode='r') as f:
        if truncate:slovar.truncate()#Опустошаем таблицу базы данных, если надо
        i,j,k=0,0,0#Счетчик строк в файле и записей в базе данных
        #файл большой, поэтому читаем его блоками по 10000 строк
        nbl=10000
        block=[f.readline()]
        while block[-1]:
            block=[block[-1]]
            [block.append(f.readline()) for ii in range(nbl)]
            i+=nbl
            #блок должен заканчиваться на строке "\n" либо на символе конца файла, проверяем и читаем дальше, пока не найдем эту строку
            while block[-1]!="\n" and block[-1]!="":
                block.append(f.readline())
                i+=1
            #Приступаем к поиску слов в блоке текста и вставке в базу
            blocktext="".join(block)
            inserted,updated=parse_dsl(blocktext)
            j+=inserted
            k+=updated
            print '!clear!Добавлено {0:d} слов, обновлено {1:d} готовность словаря {2:.2%}'.format(j,k,float(i)/n)#!clear! спецкоманда работнику для очистки вывода
            db.commit()
        f.close()
        db.commit()
        return "Complite"

def indexing():
    db=current.db
    db.executesql('CREATE INDEX IF NOT EXISTS slovoidx ON slovar (slovo);')
    db.executesql('CREATE INDEX IF NOT EXISTS pinyinidx ON slovar (pinyin);')
    db.executesql('CREATE INDEX IF NOT EXISTS perevodidx ON slovar (perevod);')
    return "Индексация выполнена"

def createlinks():
    """Создание ссылок между записями словарных статей"""
    slovar=current.slovar
    db=current.db
    reg_ref=re.compile(r"\[ref\](.*?)\[/ref\]")
    i,j=0,0
    n=db(slovar.id>0).count()
    for x in db(slovar.id>0).iterselect():
        i+=1
        for slovlnk in reg_ref.findall(x.perevod):
            row=db(slovar.slovo==slovlnk).select().first()
            if row==None:continue

            tolist=x.linksto if x.linksto!=None else []
            if row.id not in tolist:
                tolist.append(row.id)
                x.update_record(linksto=tolist)

            fromlist=row.linksfrom if row.linksfrom!=None else []
            if x.id not in fromlist:
                fromlist.append(x.id)
                row.update_record(linksfrom=fromlist)
            j+=1
        if j%1000==0:db.commit()#Фиксируем каждые 1000 вставок
        print '!clear!Ссылок найдено {0:d}. Готовность {1:.2%}'.format(j,float(i)/n)
    db.commit()
    return "Complite"

def calc_records():
    """Расчет записей для вычисляемых полей"""
    slovar=current.slovar
    db=current.db
    #Список объектов вычисляемых полей
    to_compute=[ofield for ofield in slovar if ofield.compute]
    if to_compute:
        i=0
        rows=db(slovar.id>0)
        n=rows.count()
        for x in rows.iterselect():
            i+=1
            x.update_record(**{ofield.name:ofield.compute(x) for ofield in to_compute})
            if i%10000==0:db.commit()#Фиксируем каждые 10000 обновлений
            print '!clear!Расчет записи с id={0:d}. Готовность {1:.2%}'.format(x.id,float(i)/n)
        db.commit()
    return "Complite"

def choiselist():
    """Заполнение списка вариантов перевода"""
    from bkrstools import sokr_perevod
    slovar=current.slovar
    db=current.db
    i=0
    rows=db(slovar.choiselist==[])
    n=rows.count()
    for x in rows.iterselect(slovar.id,slovar.slovo,slovar.perevod,slovar.choiselist):
        i+=1
        print '!clear!Анализ перевода слова id={0:d}. Готовность {1:.2%}'.format(x.id,float(i)/n)
        slovlist=sokr_perevod(x.perevod,x.slovo).elements('li')
        if slovlist!=None:
            x.update_record(choiselist=[y.flatten() for y in slovlist])
        if i%10000==0:db.commit()#Фиксируем каждые 10000 обновлений
    db.commit()
    return "Complite"

def extract_examles():
    """Извлечение примеров из словаря"""
    slovar=current.slovar
    db=current.db
    i,j,k,l=0,0,0,0
    rows=db((slovar.with_examples==True)&(slovar.is_example==False)&(slovar.processed==False))
    n=rows.count()
    for x in rows.iterselect(slovar.id,slovar.perevod):
        i+=1
        updated,inserted=extract_save_examples(x.perevod,x.id)
        j+=updated+inserted
        k+=updated
        l+=inserted
        print '!clear!Cлово id={0:d}. Готовность {1:.2%} Найдено {2:d}. Обновлено {3:d}. Вставлено {4:d}'.format(x.id,float(i)/n,j,k,l)
        x.processed=True
        x.update_record()
        #if j%10000==0:db.commit()#Фиксируем каждые 10000 обновлений
        db.commit()
    return "Complite"

from bkrstools import extract

def extract_save_examples(perevod,id=None):
    """Извлечение и сохранение примеров из перевода"""
    slovar=current.slovar
    db=current.db
    exlist=extract(perevod)
    updated,inserted=0,0
    for exam in exlist:
        try:
            slovar.insert(
                slovo=exam.slovo,
                pinyin=exam.pinyin,
                perevod=exam.perevod,
                linksfrom=[id] if id else [],
                is_example=True)
            inserted+=1
        except:
            db.commit()
            row=db(slovar.slovo==exam.slovo).select().first()
            if not row:continue
            if id and id not in row.linksfrom: row.linksfrom.append(id)
            if exam.perevod not in row.perevod.decode('utf-8'):
                row.perevod=row.perevod.decode('utf-8')+u"[apndx]"+exam.perevod+u"[/apndx]"
                row.with_appendix=True
                row.update_record()
                updated+=1
    return updated,inserted

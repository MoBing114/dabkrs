#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import re
from BeautifulSoup import BeautifulSoup as bs

reg_ref=re.compile(r"\[ref\](.*?)\[/ref\]")#A()
reg_c=re.compile(r"\[c\](.*?)\[/c\]")#SPAN()
colors=['green','brown','violet','red','crimson','black','gray']
reg_ccolors={color:re.compile(r"\[c %s\](.*?)\[/c\]"%color) for color in colors}#SPAN()
reg_i=re.compile(r"\[i\](.*?)\[/i\]")#I()
reg_b=re.compile(r"\[b\](.*?)\[/b\]")#B()
reg_p=re.compile(r"\[p\](.*?)\[/p\]")#I()
reg_skobki=re.compile(r"(\(.*?\))")#SPAN()
reg_numerate=re.compile(r"([^\d])(\d{1,2})[).]")#SPAN()
reg_alfavite=re.compile(u"([^a-zа-я]+[abcdeабвгд])\)")#SPAN()
reg_m=re.compile(r"\[m([1-4])\](.*?)\[/m\]")#DIV()
reg_e=re.compile(r"\[e\](.*?)\[/e\]")#DIV()
reg_ex=re.compile(r"\[ex\](.*?)\[/ex\]")#DIV()
reg_x=re.compile(r"\[\*\](.*?)\[/\*\]")#DIV()
reg_mi=re.compile(r"(\[m[1-4]\])")

def normalise_perevod(text):
    """Функция устраняет незакрытые или неоткрытые тэги (то, что в квадр.скобках [команды, метки]) синтаксиса словарной статьи, а также преобразует кодировку в 'utf-8' во избежание проблем с кодировкой"""
    perevod=unicode(text, 'utf-8')
    perevod=perevod.replace("[m1]-----[/m]","[m1]")
    perevod=perevod.replace("([i]","[i](")
    perevod=perevod.replace("[/i])",")[/i]")
    perevod=perevod.replace("([c]","[c](")
    perevod=perevod.replace("[/c])",")[/c]")
    perevod=perevod.replace("[i];[/i]",";")
    perevod1=[]#Список отбработанных частей
    #разобъем строку по закрывающему тэгу абзаца "[/m]"
    for x in perevod.split("[/m]"):
        x=x.strip()#Подрезаем кончики
        if x=="":continue#Исключаем пустые
        x=reg_mi.sub(r"[/m]\1",x)#Заменяем открывающие тэги абзаца на тот же тэг с закрывающим тэгом в начале
        for y in x.split("[/m]"):#разобъем строку по закрывающему тэгу абзаца "[/m]"
            y=y.strip()#Подрезаем кончики
            if y=="":continue#Исключаем пустые
            if reg_mi.search(y)==None:y="[m1]"+y#Если открывающего тэга абзаца нет, то ставим его в начале
            perevod1.append(y)#Добавляем в список отбработанных частей
        #В итоге полученный список должен содержать элементы начинающиеся с откр.тэга абзаца
        #Добавляем закрывающий тэг абзаца к каждому элементу списка, сцепляем элементы и возвращаем строку
    return "".join([x+"[/m]" for x in perevod1 if x.strip()!=""])

def repres_perevod(perevod,*args):
    """Функция создает html представление синтаксиса словарной стати, путем замены соответствующих тэгов"""
    #Нормализуем словарную статью
    perevod=normalise_perevod(perevod)
    #Текст может содержать тэги ссылок, создадим ссылку на действие контроллера slovo для обработки нажатия этих ссылок
    link=URL("slovo")
    perevod=reg_ref.sub(r"<a href='%s\?slovo=\1' slovo='\1'>\1</a>"%link,perevod)#Заменяем тэги ссылок [ref] на html тэги
    perevod=reg_alfavite.sub(r"<span'>\1.</span>",perevod)#Выделяем буквенное перечисление
    perevod=reg_numerate.sub(r"\1<span'>\2.</span>",perevod)#Выделяем нумерованное перечисление
    perevod=reg_c.sub(r"<span>\1</span>",perevod)#Заменяем тэги выделения на html тэги
    for color,reg_ccolor in reg_ccolors.items():
        perevod=reg_ccolor.sub(r"<span class='%s'>\1</span>"%color,perevod)#Заменяем тэги выделения цветом на html тэги
    perevod=reg_skobki.sub(r"<span>\1</span>",perevod)#Всё что в скобках обозначаем как span
    perevod=reg_i.sub(r"<i class='green'>\1</i>",perevod)#Заменяем тэги курсива [i] на html тэги
    perevod=reg_p.sub(r"<i class='green'>\1</i>",perevod)#Заменяем тэги пометок [p] на html тэги
    perevod=reg_b.sub(r"<b>\1</b>",perevod)#Заменяем тэги жирным [b] на html тэги
    perevod=reg_m.sub(r"<div class='m\1'>\2</div>",perevod)#Заменяем тэги абзацев [m1~4] на html тэги
    perevod=reg_e.sub(r"<div class='ex'>\1</div>",perevod)#Заменяем тэги примера [e] на html тэги
    perevod=reg_ex.sub(r"<div class='ex'>\1</div>",perevod)#Заменяем тэги примера [ex] на html тэги
    perevod=reg_x.sub(r"<div class='ex'>\1</div>",perevod)#Заменяем тэги примера [*] на html тэги
    perevod=perevod.replace("\[","<span>[")#Заменяем экранирование спецсимвола синтаксиса словарной статьи
    perevod=perevod.replace("\]","]</span>")#Заменяем экранирование спецсимвола синтаксиса словарной статьи
    perevod=re.sub(r"<div class='m[1-4]'>\s*</div>","",perevod)#Удаляем пустые блоки(содержащие пробельные символы)

    return TAG(bs(perevod).prettify())#Создаем экземпляр класса TAG путем парсинга текста, предварительно пропустив его через BeautifulSoup

def split_perevod(div,slovo):
    """Разбивает текст в блоках div сласса m[1-4] на варианты перевода в зависимости от вида разделителя ("," или ";") и возвращает элементы списка LI"""
    text=div.flatten().strip()
    sep=","
    if ";" in text or re.search(u"[，、。]",slovo)!=None:sep=";"
    return CAT(*[LI(x.strip()) for x in text.split(sep) if x.strip()!=""])

def sokr_perevod(perevod,slovo,*args):
    """Функция очищает, сокращает html представление словарной статьи путем замены соответствующих тэгов"""
    tagObj=repres_perevod(perevod)#Возвращает уже объект класса TAG, а не текст
    #slovo=unicode(slovo, 'utf-8')#В юникод сразу, чтобы не было проблем
    perevod_po_silke=[]
    for ref in tagObj.elements('a'):
        ref_perevod=current.db(current.slovar.slovo==ref["_slovo"]).select(current.slovar.perevod).first()
        if ref_perevod!=None:
            perevod_po_silke.append(repres_perevod(ref_perevod.perevod))
    tagObj.append(CAT(*perevod_po_silke))
    tagObj.elements('a',replace=None)
    tagObj.elements('div.ex', replace=None)#Убираем примеры
    tagObj.elements('i', replace=None)#Убираем курсив
    tagObj.elements('span', replace=None)#Убираем разрывы
    tagObj.elements('b', replace=None)#Убираем жирный
    tagObj.elements('div',_class=re.compile(r'm[1-4]'),replace=lambda div: "" if div.flatten().strip()=="" else div)#Удаляем пустые блоки
    tagObj.elements('div',_class=re.compile(r'm[1-4]'),replace=lambda div: split_perevod(div,slovo))#Непустые блоки преобразуем в элементы списка
    values=[]
    for value in [x.flatten().strip() for x in tagObj.elements('li')]:
        if not value in values: values.append(value)
    tagObj=UL(values)
    return tagObj

re_pass=re.compile(u"[ 。.а-яёА-ЯЁa-zA-Z0-9（ ）【 】～！”“；：《》<>=+\-]")#Группа символов, содержащие символы в скобках, пропускается

def text_tokenizer(txt):
    """Разбирает на отдельные иеролифы(символы) или их возможные сочетания(состоящие из 1 до n-1 символов)"""
    txt=txt.decode()
    maxn=15#Макс.длина слова
    n=len(txt)#Длина текста
    l=n if n<maxn else maxn
    slovlist={}#Словарь со словами в ключах и списком координат в тексте (диапазона)
    for i in range(1,l+1):
        for j in range(i):
            for x in re.finditer(r".{%d}"%(i),txt[j:]):
                key=x.group(0)
                if re_pass.search(key)!=None:continue
                value=[(x.start()+j,x.end()+j)]
                if key in slovlist:
                    slovlist[key].extend(value)
                else:
                    slovlist[key]=value
    return slovlist

from gluon.storage import Storage#Аналог словаря, ведет как словарь, ключи являются атрибутами, но не вызывает исключения при отсутсвии ключа, а просто выдает None
from itertools import takewhile

def reshala(text):
    #text=unicode(text, 'utf-8')#Декодируем строку на всякий случай
    db=current.db
    slovar=current.slovar
    #Пробуем найти всю строку
    row=db(slovar.slovo==text).select().first()
    if row!=None:
        bolvanka=[
            Storage(
                slovo=unicode(row.slovo, 'utf-8'),
                pinyin=row.pinyin,
                perevod=row.perevod,
                start=0,
                end=len(unicode(row.slovo, 'utf-8')),
                dlina=len(unicode(row.slovo, 'utf-8'))
            )
        ]
        return bolvanka
    #Если не найдено до переходим к пословному поиску
    slovlist=text_tokenizer(text)
    bolvanka=Storage()
    for key,positions in slovlist.items():
        y=db(slovar.slovo==key).select().first()
        if y==None:continue
        for start,end in positions:
            value=Storage(
                    slovo=y.slovo,
                    pinyin=y.pinyin,
                    perevod=y.perevod,
                    start=start,
                    end=end,
                    dlina=end-start
                )
            if bolvanka[start]==None:
                bolvanka[start]=value
            elif value.dlina>bolvanka[start].dlina:
                bolvanka[start]=value
    if bolvanka[0]==None:return bolvanka
    n=len(text)
    for i in range(n):
        if i not in bolvanka:
            bolvanka[i]=Storage(
                slovo=text[i],
                pinyin="",
                perevod=None,
                start=i,
                end=i+1,
                dlina=1
            )
    i=0
    while i<n:
        if bolvanka[i].perevod==None and bolvanka[i-1].perevod!=None:
            start=i
            i+=1
        elif bolvanka[i].perevod==None:
            bolvanka[start].slovo+=bolvanka[i].slovo
            bolvanka[start].perevod=""
            bolvanka[start].end+=1
            bolvanka[start].dlina+=1
            i+=1
        else:
            i+=1
    nabor={i:"|"+"|".join(str(x) for x in range(i,bolvanka[i].end))+"|" for i in bolvanka.keys()}
    for i,x in nabor.items():
        for j,y in nabor.items():
            if y in x and y!=x: bolvanka[j].perevod=None
    for key,value in bolvanka.items():
        if value.perevod==None:
            del bolvanka[key]
    bolvanka=list(bolvanka.values())
    bolvanka.sort(key=lambda x:x.start)
    return bolvanka

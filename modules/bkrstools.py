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
reg_mnone=re.compile(r"(^.*?)(\[m[1-4]\])")#DIV()
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
    perevod=reg_c.sub(r"<span>\1</span>",perevod)#Заменяем тэги выделения на html тэги
    for color,reg_ccolor in reg_ccolors.items():
        perevod=reg_ccolor.sub(r"<span class='%s'>\1</span>"%color,perevod)#Заменяем тэги выделения цветом на html тэги
    perevod=reg_i.sub(r"<i class='green'>\1</i>",perevod)#Заменяем тэги курсива [i] на html тэги
    perevod=reg_b.sub(r"<b>\1</b>",perevod)#Заменяем тэги жирным [b] на html тэги
    perevod=reg_p.sub(r"<i class='green'>\1</i>",perevod)#Заменяем тэги пометок [p] на html тэги
    perevod=reg_m.sub(r"<div class='m\1'>\2</div>",perevod)#Заменяем тэги абзацев [m1~4] на html тэги
    perevod=reg_e.sub(r"<div class='ex'>\1</div>",perevod)#Заменяем тэги примера [e] на html тэги
    perevod=reg_ex.sub(r"<div class='ex'>\1</div>",perevod)#Заменяем тэги примера [ex] на html тэги
    perevod=reg_x.sub(r"<div class='ex'>\1</div>",perevod)#Заменяем тэги примера [*] на html тэги
    perevod=re.sub(r"<div class='m[1-4]'> *</div>","",perevod)#Удаляем пустые блоки
    perevod=perevod.replace("\[","[")#Заменяем экранирование спецсимвола синтаксиса словарной статьи
    perevod=perevod.replace("\]","]")#Заменяем экранирование спецсимвола синтаксиса словарной статьи
    return DIV(TAG(bs(perevod).prettify()),_class="ru")

def create_spisok(text,*args):
    """Функция очищает html представление словарной стати путем замены соответствующих тэгов"""
    text=repres_perevod(text)
    text.elements('a',
                  replace=lambda ref:
                  DIV(*[repres_perevod(x[0].perevod)[:] for x in [db(slovar.slovo==ref["_slovo"]).select(slovar.perevod)] if x!=None],_class="links")
                 )
    text.elements('div.ex', replace=None)#Убираем примеры
    text.elements('i', replace=None)#Убираем курсив
    text.elements('span', replace=None)#Убираем разрывы
    text.elements('b', replace=None)#Убираем жирный
    text.elements('div',_class=re.compile(r'm[1-4]'),replace=lambda div: "" if div.flatten().strip()=="" else div)#Удаляем пустые блоки
    return text

def text_tokenizer(txt):
    #Разбирает на отдельные иеролифы(символы) или их возможные сочетания(состоящие из 1 до n-1 символов)
    txt=txt.decode()
    n=len(txt)
    if n==1:return [txt]
    x=range(n)
    rez=[]
    for g in x:
        for i in x:
            if i+g>n or i==i+g:continue
            rez.append(txt[i:i+g])
    return set(rez)

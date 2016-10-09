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
reg_alfavite=re.compile(u"([^a-zа-я]+)([abcdeабвгд])\)")#SPAN()
reg_m=re.compile(r"\[m([1-4])\](.*?)\[/m\]")#DIV()
reg_e=re.compile(r"\[e\](.*?)\[/e\]")#DIV()
reg_ex=re.compile(r"\[ex\](.*?)\[/ex\]")#DIV()
reg_x=re.compile(r"\[\*\](.*?)\[/\*\]")#DIV()
reg_mi=re.compile(r"(\[m[1-4]\])")

def normalise_perevod(text):
    """Функция устраняет незакрытые или неоткрытые тэги (то, что в квадр.скобках [команды, метки])
    синтаксиса словарной статьи, а также преобразует кодировку в 'utf-8' во избежание проблем с кодировкой"""
    if not isinstance(text,unicode):perevod=unicode(text, 'utf-8')
    #Эранируем управл. символы html, если они есть в тексте
    perevod=perevod.replace("&","&amp;")#Амперсанд
    perevod=perevod.replace(">","&gt;")#Больше
    perevod=perevod.replace("<","&lt;")#Меньше
    perevod=perevod.replace("'","&apos;")#Апостроф
    perevod=perevod.replace('"',"&quot;")#Кавычка
    #Очищаем или преобразуем некоторые конструкции синтаксиса словаря
    perevod=perevod.replace("[m1]-----[/m]","[m1]")
    perevod=perevod.replace("([i]","[i](")#Открыв.скобку во внутрь
    perevod=perevod.replace("[/i])",")[/i]")#Закр.скобку во внутрь
    perevod=perevod.replace("([c]","[c](")
    perevod=perevod.replace("[/c])",")[/c]")
    perevod=perevod.replace("[i];[/i]",";")
    perevod=perevod.replace("[*][ex]","[ex]")
    perevod=perevod.replace("[/ex][/*]","[/ex]")
    #Проверка соблюдения правил вложенности
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
        #В итоге полученный список perevod1 должен содержать элементы начинающиеся с откр.тэгов абзаца [m1]-[m4]
        #Добавляем закрывающий тэг абзаца [/m] к каждому элементу списка в конец, сцепляем элементы и возвращаем строку
    return "".join([x+"[/m]" for x in perevod1 if x.strip()!=""])

def repres_perevod(perevod,*args):
    """Функция создает html представление синтаксиса словарной стати, путем замены соответствующих тэгов"""
    #Нормализуем словарную статью
    perevod=normalise_perevod(perevod)
    #Текст может содержать тэги ссылок, создадим ссылку на действие slovo контроллера slovar для обработки нажатия этих ссылок
    link=URL(c="slovar",f="slovo")
    perevod=reg_ref.sub(r"<a href='%s\?slovo=\1' slovo='\1'>\1</a>"%link,perevod)#Заменяем тэги ссылок [ref] на html тэги
    perevod=reg_alfavite.sub(r"\1<span'>\2.</span>",perevod)#Выделяем буквенное перечисление
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

    return TAG(bs(perevod).renderContents())#Создаем экземпляр класса TAG путем парсинга текста, предварительно пропустив его через BeautifulSoup

def cut_perevod(perevod,*args):
    """Функция убирает примеры из html представления словарной статьи"""
    tagObj=repres_perevod(perevod)#Возвращает уже объект класса TAG, а не текст
    tagObj.elements('div.ex', replace=None)#Убираем примеры
    tagObj.elements('div',_class=re.compile(r'm[1-4]'),replace=lambda div: "" if div.flatten().strip()=="" else div)#Удаляем пустые блоки
    return tagObj

def split_perevod(div,slovo):
    """Разбивает текст в блоках div сласса m[1-4] на варианты перевода в зависимости от вида разделителя ("," или ";") и возвращает элементы списка LI"""
    text=div.flatten().strip()
    sep=","
    if ";" in text or re.search(u"[，、。]",slovo)!=None:sep=";"
    return CAT(*[LI(x.strip()) for x in text.split(sep) if x.strip()!=""])

def sokr_perevod(perevod,slovo,*args):
    """Функция создает список вариантов перевода"""
    if not isinstance(slovo,unicode):slovo=unicode(slovo, 'utf-8')
    tagObj=repres_perevod(perevod)#Возвращает уже объект класса TAG, а не текст
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
        if not value in values and re.search(u"[一-龥]",unicode(value, 'utf-8'),re.U)==None: values.append(value)
    tagObj=UL(values)
    return tagObj

re_pass=re.compile(u"[ 。.а-яёА-ЯЁa-zA-Z0-9（ ）【 】～！”“；：《》<>=+\-]")#Группа символов, содержащие символы в скобках, пропускается

def text_tokenizer(txt):
    """Разбирает на отдельные иеролифы(символы) или их возможные сочетания(состоящие из 1 до n-1 символов)"""
    #txt=txt.decode()
    maxn=15#Макс.длина слова
    n=len(txt)#Длина текста
    l=n if n<maxn else maxn
    slovdict={}#Словарь со словами в ключах и списком координат в тексте (диапазона)
    for i in range(1,l+1):
        for j in range(i):
            for x in re.finditer(r".{%d}"%(i),txt[j:]):
                key=x.group(0)
                if re_pass.search(key)!=None:continue
                value=[(x.start()+j,x.end()+j)]
                if key in slovdict:
                    slovdict[key].extend(value)
                else:
                    slovdict[key]=value
    return slovdict

from gluon.storage import Storage
#Класс Storage - аналог словаря dict, ведет как словарь, ключи являются атрибутами(если строчные), но не вызывает исключения при отсутсвии ключа, а просто выдает None


def reshala(text):
    """Выдает список найденых в базе словаря объектов, представляющих слова и содержащихся в запрашиваемом тексте в порядке их следования"""
    if not isinstance(text,unicode):text=unicode(text, 'utf-8') #Преобразуем строку типа str в тип unicode 'utf-8'
    db=current.db
    slovar=current.slovar
    n=len(text)#Длина текста, пригодится еще
    #Объект исходного текста, добавим его в начало списка перед выводом
    ishodnik=Storage(slovo=text,pinyin="",perevod="",start=0,end=n,dlina=n,childs=[])
    #Словарь из комбинаций иероглифов в ключах и позициями данной комбинации в значениях (кортеж)
    slovdict=text_tokenizer(text)
    #Пробуем найти весь текст
    row=db(slovar.slovo==text).select().first()
    if row!=None:
            ishodnik.id=row.id
            ishodnik.pinyin=row.pinyin
            ishodnik.perevod=row.perevod
            ishodnik.choiselist=row.choiselist
            if text in slovdict:slovdict.pop(text)
    #Переходим к пословному поиску
    #Заготовка в виде экземпляра Storage, ключ - позиция первого символа слова в тексте, значение - объект представления слова (экз. Storage)
    bolvanka=Storage()
    for key,positions in slovdict.items():
        #Запрашиваем в базе
        row=db(slovar.slovo==key).select().first()
        if row==None:continue#Если нет, то берем следущее слово
        #Слово есть в базе, но оно может несколько раз встречаться в тексте, поэтому пройдемся по этим местам
        for start,end in positions:
            #Подготовим объект, представляющий слово (со всем содержимым экземпляра Row в переменной row, плюс атрибуты позиций и длина)
            value=Storage(
                    id=row.id,
                    slovo=unicode(row.slovo,'utf-8'),
                    pinyin=row.pinyin,
                    perevod=row.perevod,
                    choiselist=row.choiselist,
                    start=start,
                    end=end,
                    dlina=end-start,
                    childs=[]
                )
            #Если данная позиция не занята, то заполняем
            if bolvanka[start]==None:
                bolvanka[start]=value
            #Если занята, то заполняем самым длинным словом, старое тащим к детям
            elif value.dlina>bolvanka[start].dlina:
                value.childs.extend(bolvanka[start].childs)
                bolvanka[start].childs=[]
                value.childs.append(bolvanka.pop(start))
                bolvanka[start]=value
            else:
                bolvanka[start].childs.append(value)
    #Если в базе вообще ничего не найдено, то возвращаем список с исходником
    if bolvanka.keys()==[]:return [ishodnik]
    #Заполним заготовку объектами, представляющими символы текста, которые не найдены
    for i in range(n):
        if i not in bolvanka:
            bolvanka[i]=Storage(
                slovo=text[i],
                pinyin="",
                perevod=None,
                choiselist=None,
                start=i,
                end=i+1,
                dlina=1,
                childs=[]
            )
    #Помечаем первый символ группы непрерывной последовательности символом без перевода атрибутом .perevod="",
    #а всю последовательность символов в группе переносим в первый символ
    for x in re.finditer("1+","".join(['1' if val.perevod==None else '0' for val in bolvanka.values()])):
        start=x.start()
        bolvanka[start].perevod=""
        for key in range(x.start()+1,x.end()):
            bolvanka[start].slovo+=bolvanka[key].slovo
            bolvanka[start].end+=1
            bolvanka[start].dlina+=1
    #Найдем ключи с вложенными диапазонами
    #Вспомогательный словарь из множеств - раскрытых диапазонов позиций символов слова
    nabor={i:set(range(i,bolvanka[i].end)) for i in bolvanka.keys()}
    for pkey,x in nabor.items():
        if bolvanka[pkey]==None:continue
        for ckey,y in nabor.items():
            if bolvanka[ckey]==None:continue
            if y < x and bolvanka[ckey].perevod!=None:
                bolvanka[pkey].childs.extend(bolvanka[ckey].childs)
                bolvanka[ckey].childs=[]
                bolvanka[pkey].childs.append(bolvanka.pop(ckey))
    #Удаляем ключи с .perevod==None
    for key,value in bolvanka.items():
        if value.perevod==None:
            del bolvanka[key]

    #Преобразуем в список, сортируем
    bolvanka=list(bolvanka.values())
    bolvanka.sort(key=lambda x:x.start)
    #Найдем иероглифы на стыке
    for i in xrange(len(bolvanka)-1):
        a=bolvanka[i]
        b=bolvanka[i+1]
        ar=set(range(a.start,a.end))
        br=set(range(b.start,b.end))
        ab=list(ar&br)
        ab.sort()
        ar=list(ar)
        br=list(br)
        ar.sort()
        br.sort()
        if ab!=[]:
            aa,bb= ab[0]-ar[-1]-1,ab[-1]-br[0]+1
            a.rspan=aa#Отриц.число, обозначает сколько символов с конца имеются в следующем слове slovo[rspan:]
            b.lspan=bb#Полож.число, обозначает сколько символов с начала имеются в предыдущим слове slovo[:lspan]

    bolvanka.insert(0,ishodnik)
    return bolvanka

def splitby(spisok,ngroup):
    """Разбивает список на подсписки из заданного числа элементов"""
    newspisok=[]
    i=1
    x=[]
    while spisok!=[]:
        if i>ngroup:
            newspisok.append(x)
            x=[]
            i=1
        x.append(spisok.pop(0))
        i+=1
        if spisok==[]:newspisok.append(x)
    return newspisok

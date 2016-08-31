# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bkrstools import text_tokenizer

def index():
    """Действие по умолчанию, показывает таблицу словарной базы данных"""
    form=SQLFORM.grid(
        slovar,
        user_signature=False,
        #fields=[slovar.slovo,slovar.pinyin,slovar.perevod,slovar.spisok],
    )
    return dict(form=form)

def slovo():
    """Действие просмотра слова, перенаправляет на страницу просмотра при клике по ссылке"""
    row=db(slovar.slovo==request.vars.slovo).select().first()
    if row!=None: redirect(URL('index',args=('view','slovar',row.id)))#Временно используется форма действия index данного контроллера

def text():
    """Действие создает поисковую форму, обрабатывает полученный текст и передает выборку из базы данных в представление"""
    #Поисковая форма
    form = FORM(INPUT(_id="w2p_keywords",_type="text",_name="text",_class="form-control",_value=request.vars.text),#Поле ввода текста
                    INPUT(_type="submit",_class="btn btn-default",_value="Поиск"),#Кнопка "поиск"
                    keepvalues=True,#Удерживать значения
                    _class="form-search", _action=URL('text')#Класс готового стиля оформления и действие контроллера, который обработает нажатие кнопки (которое в общем то и создает форму)
                   )
    rez=[]
    text=""
    if form.process().accepted:#Обработка нажатия кнопки формы поиска
        text=unicode(request.vars.text, 'utf-8')#Декодируем строку на всякий случай
        rez=db(slovar.slovo==text).select().first()#Пробуем найти всю строку
        if rez!=None:
            rez=[[rez.slovo,rez.pinyin,rez.perevod,1]]
            return dict(form=form, rez=rez, text=text)
        rez={unicode(y.slovo, 'utf-8'):[y.pinyin,y.perevod]
             for y in [db(slovar.slovo==sl).select().first()
                       for sl in text_tokenizer(text)] if y!=None}

        z={i:[x for x in rez.keys() if text[i:i+len(x)]==x] for i in range(len(text))}

        for i in z.keys():
            z[i].sort(key=len,reverse=True)
            if z[i]!=[]:
                z[i]=z[i][0]
            else:
                z[i]=text[i]

        nabor={i:"|"+"|".join(str(x) for x in range(i,i+len(z[i])))+"|" for i in z.keys()}
        for i,x in nabor.items():
            for j,y in nabor.items():
                if y in x and y!=x: z[j]=""

        rez=[[slovo,rez.get(slovo,["",""])[0],rez.get(slovo,["",""])[1],i] for i,slovo in z.items() if slovo!=""]
    return dict(form=form, rez=rez, text=text)

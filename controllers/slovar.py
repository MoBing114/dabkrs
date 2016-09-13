# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bkrstools import text_tokenizer,repres_perevod,sokr_perevod,reshala

def index():
    """Действие по умолчанию, показывает таблицу словарной базы данных"""
    form=SQLFORM.grid(
        slovar,
        csv=False,
        #fields=[slovar.slovo,slovar.pinyin,slovar.perevod,slovar.spisok],
    )
    return dict(form=form)

def slovo():
    return dict(ajaxotvet=otvet())


def otvet():
    if request.vars.slovo==None:return ""
    if isinstance(request.vars.slovo,list):request.vars.slovo=request.vars.slovo[-1]
    text=unicode(request.vars.slovo, 'utf-8')#Декодируем строку на всякий случай
    rez=reshala(text)
    proc_func=repres_perevod if len(rez)==1 else sokr_perevod
    return CAT(DIV(request.vars.slovo,_class="iskomyi-text"),
               *[DIV(A(DIV(x.slovo,_class="ch"),_href=URL("slovo",vars=dict(slovo=x.slovo))),
            DIV(x.pinyin,_class="py"),
            DIV(proc_func(x.perevod,x.slovo),_class="ru"),
            _class="slovo",
            _position=str(x.start)+"-"+str(x.end),
            _slovo=x.slovo) for x in rez])

# -*- coding: utf-8 -*-
def index(): return dict(message="hello from translater.py")

def selectform():
    form = FORM(
        INPUT(_name='slovo', _placeholder="Введите здесь текст для пословного перевода ...", _id="w2p_keywords", _class="form-control", _required=""),
        INPUT(_type='submit', _value="Искать", _class="btn"),
        _id="forma-poiska",
        _action=""
    )
    rows=[]
    if form.process().accepted:
        if request.vars.id!=None:
            sl=slovar(request.vars.id)
            if sl!=None:request.vars.slovo=sl.slovo
        if request.vars.slovo==None:return ""
        if isinstance(request.vars.slovo,list):request.vars.slovo=request.vars.slovo[-1]
        text=unicode(request.vars.slovo, 'utf-8')#Декодируем строку на всякий случай
        rows=reshala(text)#Расчленение текста и выдача списка найденных слов в базе
        #rows=db(slovar.id<20).select()
    return dict(form=form,rows=rows)
from gluon.tools import Crud
crud = Crud(db)

def display_form():
    crud.settings.update_next=None
    form=crud.update(slovar,request.vars.id)
    return form

# -*- coding: utf-8 -*-
def index():
    form = FORM(
        INPUT(_name='slovo', _placeholder="Введите здесь текст для пословного перевода ...", _id="w2p_keywords", _class="form-control", _required=""),
        INPUT(_type='submit', _value="Искать", _class="btn"),
        _id="forma-poiska",
        _action=""
    )
    rows=[]

    if form.process().accepted or request.vars.slovo!=None:
        response.flash=None
        text=unicode(request.vars.slovo, 'utf-8')#Декодируем строку на всякий случай
        rows=reshala(text)#Расчленение текста и выдача списка найденных слов в базе

    return locals()

def selectform():
    form = FORM(
        INPUT(_name='slovo', _placeholder="Введите здесь текст для пословного перевода ...", _id="w2p_keywords", _class="form-control", _required=""),
        INPUT(_type='submit', _value="Искать", _class="btn"),
        _id="forma-poiska",
        _action=""
    )
    rows=[]

    if form.process().accepted or request.vars.slovo!=None:
        response.flash=None
        text=unicode(request.vars.slovo, 'utf-8')#Декодируем строку на всякий случай
        rows=reshala(text)#Расчленение текста и выдача списка найденных слов в базе

    return locals()

from gluon.tools import Crud
crud = Crud(db)

def editform():
    response.view='translater/editform.load'
    form=crud.update(slovar,request.args(0),next=URL(f='viewrecord',args=request.args))
    return dict(form=form)

def viewrecord():
    response.view='translater/editform.load'
    form=crud.read(slovar,request.args(0))
    return dict(form=form)

def getedit():
    return dict(load=LOAD(url=URL(f='editform.load',args=request.args),ajax=True,target="slovar_edit_form"))
def jeditable():
    
    return dict()

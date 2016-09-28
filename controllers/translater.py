# -*- coding: utf-8 -*-
def index(): return dict(message="hello from translater.py")

def display_form():
    record = 2#slovar(request.args(0)) or redirect(URL('index'))
    form = SQLFORM(slovar, record)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def selectforv():
    rows=db(slovar.id<20).select(slovar.choiselist)
    form=DIV(*[SELECT(row.choiselist) for row in rows],_class="col-md-4")
    form.append(STYLE("select{-webkit-appearance: none;-moz-appearance: none;appearance: none;border:none;}select::-ms-expand{display: none;}"))
    return dict(form=form)

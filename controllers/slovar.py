# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bkrstools import text_tokenizer,repres_perevod,sokr_perevod,reshala,splitby

def index():
    """Действие по умолчанию, показывает таблицу словарной базы данных"""
    form=SQLFORM.grid(
        slovar,
        csv=False,
        #fields=[slovar.slovo,slovar.pinyin,slovar.perevod,slovar.spisok],
    )
    return dict(form=form)

def slovintersection(x):
    return CAT(SPAN(x.slovo[:x.lspan],_class="l-sctn") if x.lspan!=None else "",
               SPAN(x.slovo[x.lspan:x.rspan],_class="m-sctn") if x.rspan!=None or x.lspan!=None else SPAN(x.slovo,_class="m-sctn"),
               SPAN(x.slovo[x.rspan:],_class="r-sctn") if x.rspan!=None else "")

#@cache.action(cache_model=cache.ram)
def slovo():
    #response.js ="jQuery('.slovo').on('mouseenter', function() {        jQuery('.iskomyi-text').unhighlight();        var v = jQuery(this).attr('slovo');        if (v!='') jQuery('.iskomyi-text').highlight(v);    });    jQuery('.slovo').on('mouseleave', function() {        jQuery('.iskomyi-text').unhighlight();    });"
    return dict(ajaxotvet=otvet())


def otvet():
    if request.vars.slovo==None:return ""
    if isinstance(request.vars.slovo,list):request.vars.slovo=request.vars.slovo[-1]
    text=unicode(request.vars.slovo, 'utf-8')#Декодируем строку на всякий случай
    rez=reshala(text)
    first=rez.pop(0)
    first=DIV(
        DIV(first.slovo,_class="ch2"),
        DIV(first.pinyin,_class="py"),
        DIV(repres_perevod(first.perevod,first.slovo),_class="ru"),
        _class="iskomyi-text",
        )
    proc_func=sokr_perevod
    bywords=[DIV(A(slovintersection(x),_class="black ch",_href=URL("slovo",vars=dict(slovo=x.slovo))),
            #DIV(DIV("Дочерние слова:"),*[SPAN(A(y.slovo,_class="black ch",_href=URL("slovo",vars=dict(slovo=y.slovo))),"，") for y in x.childs],_class="childs"),
            DIV(x.pinyin,_class="py"),
            DIV(proc_func(x.perevod,x.slovo),_class="ru"),
            _class="slovo",
            _position=str(x.start)+"-"+str(x.end),
            _slovo=x.slovo) for x in rez]
    bywords=TABLE(splitby(bywords,5),_class="bywords")
    slovlist=DIV(" ".join([x.elements('li')[0].flatten() for x in bywords.elements('div.ru') if x.elements('li')!=[]]),_class="slovlist")
    return CAT(DIV("Словарный:",_class="txt-label"),first,DIV("Пословный:",_class="txt-label"),bywords,DIV("Псевдоперевод:",_class="txt-label"),slovlist)

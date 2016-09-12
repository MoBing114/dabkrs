# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bkrstools import text_tokenizer,repres_perevod,sokr_perevod

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
    rez=[]
    text=unicode(request.vars.slovo, 'utf-8')#Декодируем строку на всякий случай
    rez=db(slovar.slovo==text).select().first()#Пробуем найти всю строку
    if rez!=None:
        rez=[[rez.slovo,rez.pinyin,rez.perevod,1]]
    else:
        #Словарь с ключами из слов и значениями из списка пиньин перевод
        rez={unicode(y.slovo, 'utf-8'):[y.pinyin,y.perevod]
             for y in [db(slovar.slovo==sl).select().first()
                       for sl in list(text_tokenizer(text).keys())] if y!=None}

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
    proc_func=repres_perevod if len(rez)==1 else sokr_perevod
    return CAT(DIV(request.vars.text if request.vars.text!=None else "",_class="iskomyi-text"),*[DIV(A(DIV(x[0],_class="ch"),_href=URL("slovo",vars=dict(slovo=x[0]))),
            DIV(x[1],_class="py"),
            DIV(proc_func(x[2],x[0]),_class="ru"),
            _class="slovo",
            _position=str(x[3])+"-"+str(x[3]+len(x[0])-1),
            _slovo=x[0]) for x in rez])

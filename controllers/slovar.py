# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bkrstools import text_tokenizer

def index():
    form=SQLFORM.grid(
        slovar,
        user_signature=False,
        #fields=[slovar.slovo,slovar.pinyin,slovar.perevod,slovar.spisok],
    )
    return dict(form=form)

def slovo():
    row=db(slovar.slovo==request.vars.slovo).select().first()
    if row!=None: redirect(URL('index',args=('view','slovo',row.id)))

def text():
    form = FORM(INPUT(_id="w2p_keywords",_type="text",_name="text",_class="form-control",_value=request.vars.text),
                    INPUT(_type="submit",_class="btn btn-default",_value="Поиск"),
                    keepvalues=True,
                    _class="form-search", _action=URL('text')
                   )
    rez=[]
    text=""
    if form.process().accepted:
        text=unicode(request.vars.text, 'utf-8')
        rez=db(slovar.slovo==text).select().first()
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

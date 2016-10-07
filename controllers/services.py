# -*- coding: utf-8 -*-
from gluon.storage import Storage
def index(): return dict(message="hello from services.py")

def attrtolist(vars,*args):
    vars=Storage(vars)
    for attr in args:
        if not isinstance(vars[attr],list):vars[attr]=[vars[attr]]
        select=[]
        [select.extend(x.split(',')) for x in vars[attr] if x]
        vars[attr]=select
    return vars

@request.restful()
def api():
    response.view = 'generic.' + request.extension

    def GET(*args,**vars):
        vars=attrtolist(vars,'id','select','slovo')
        fields=Storage(id=slovar.id,slovo=slovar.slovo,perevod=slovar.perevod,dlina=slovar.dlina,choiselist=slovar.choiselist)
        fields=Storage({key:value for key,value in fields.items() if key in vars.select})
        content=[]
        if args[0]=='slovar':
            content.extend([db(slovar.id==id).select(*fields.values()).first() for id in vars.id])
            content.extend([db(slovar.slovo==slovo).select(*fields.values()).first() for slovo in vars.slovo])
        return dict(content=content)
    return locals()

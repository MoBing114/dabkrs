# -*- coding: utf-8 -*-
# попробуйте что-то вроде
def index():
    """config = dict(color='black', language=True, text="dsfdsfdsf dsfdsfds  dsfdsf")
    form = SQLFORM.dictform(config)
    if form.process().accepted:
        config.update(form.vars)
        form = SQLFORM.dictform(config)"""
    form=SQLFORM.factory(
        Field('bywords_out', 'list:string', requires=IS_NOT_EMPTY())
        )
    return dict(form=form)


def penalty():
    response.view='bywords/list.html'
    form=SQLFORM.grid(
        slovar.bywords_out==True,
        deletable=False,
        editable=False,
        details=False,
        csv=False,
    )
    return dict(form=form)


def penalty_edit():
    response.view='bywords/addedit.html'
    slovlist=db(slovar.bywords_out==True).select(slovar.slovo)
    slovlist=[x.slovo for x in slovlist] if slovlist else []
    form = FORM(
        TEXTAREA('\n'.join(slovlist),
            _name='slovlist',
            requires=IS_NOT_EMPTY(),
            _id="slov-list",
            _rows="30",
            _class="form-control",
            _placeholder="Введите список терминов"
        ),
        INPUT(_type='submit'),
        _class="form-horizontal"
    )
    if form.process().accepted:
        skiplist=request.vars.slovlist.replace(',','\n').split('\n')
        skiplist=[x.strip() for x in skiplist if x.strip()!='']
        for skip in skiplist:
            row=db(slovar.slovo==skip.strip()).select().first()
            if row:
                row.update_record(bywords_out=True)
        session.flash = 'Слова исключения добавлены'
        redirect(URL('penalty'))
    elif form.errors:
        response.flash = 'Обнаружены ошибки'
    else:
        response.title='Правка слов, исключённых из пословного перевода'
    return dict(form=form)


def short():
    response.view='bywords/list.html'
    form=SQLFORM.grid(
        slovar.use_short==True,
        deletable=False,
        editable=False,
        details=False,
        csv=False,
    )
    return dict(form=form)


def short_edit():
    response.view='bywords/addedit.html'
    slovlist=db(slovar.use_short==True).select(slovar.slovo, slovar.bywords_short)
    slovlist=[x.slovo+'\t'+x.bywords_short for x in slovlist] if slovlist else []
    form = FORM(
        TEXTAREA(
            '\n'.join(slovlist),
            _name='slovlist',
            requires=IS_NOT_EMPTY(),
            _id="slov-list",
            _rows="30",
            _class="form-control",
            _placeholder="Введите список сокращенных переводов"
        ),
        INPUT(_type='submit'),
        _class="form-horizontal"
    )
    if form.process().accepted:
        for x in request.vars.slovlist.split('\n'):
            slovo, perevod=x.split('\t')
            row=db(slovar.slovo==slovo).select().first()
            if row:
                row.update_record(bywords_short=perevod, use_short=True)
        session.flash = 'Слова с сокращенным переводом добавлены'
        redirect(URL('short'))
    elif form.errors:
        response.flash = 'Обнаружены ошибки'
    else:
        response.title='Правка слов с сокращенным переводом для использования в пословном переводе'
    return dict(form=form)

# -*- coding: utf-8 -*-
# попробуйте что-то вроде
def index():
    return dict(
        form=SQLFORM.smartgrid(
            db.scheduler_task,
            csv=False, showbuttontext=False,
            advanced_search=False
        )
               )

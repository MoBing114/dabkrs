# -*- coding: utf-8 -*-
from gluon.tools import PluginManager
from gluon.languages import translator

plugins = PluginManager('layout_starter',
                        useravatar=URL('static','plugin_layout_starter/img/avatar5.png'),
                        menu=response.menu or [],
                        admin_menu=[
        ('Admin',False,'#',[
                ('Manage Content', False, URL('content','list')),
                ('Manage Users', False, URL('appadmin','manage/users'))
                ]),
        ('Super Admin',False,'#',[
                ('Manage Auth', False,URL('appadmin','manage/auth')),
                ('Manage Database', False,URL('appadmin','manage/db')),
                ('Super Admin!', False,URL('appadmin','#'))
                ])
        ],
                        default_icon_class='fa fa-book',# icon css class, you can define css class with url to icon image, for example .myicon{content: url('/static/icons/myicon.ico')}
                        menu_icons={}, #key is menu name without T helper(used auto), value is css icon class
                        admin_menu_icons={'Admin':'fa fa-gears','Manage Content':'fa fa-file-text-o','Manage Users':'fa fa-users','Super Admin':'fa fa-gears','Manage Auth':'fa fa-wrench','Manage Database':'fa fa-database','Super Admin!':'fa fa-cog'},
                        version="1.0.0",
                        company="Plugin",
                        shortcut_icon=URL('static','plugin_layout_starter/images/favicon.ico'),
                        apple_touch_icon=URL('static','plugin_layout_starter/images/favicon.ico'),
                        logo=response.logo or XML('<i class="glyphicon glyphicon-home" aria-hidden="true"></i>'),
                        logo_mini=XML('<i class="glyphicon glyphicon-home" aria-hidden="true"></i>'),
                        seach_url="#",
                        seach_variable="keywords"
                       )
#import breadcrumbs
#breadcrumbs.append()
#from bookmark import Bookmark
#response.bookmark = Bookmark()
#useravatar=(URL(c='default',f='download',args=auth.user.avatar) if auth.user.avatar else URL('static','plugin_layout_starter/img/avatar5.png')) if auth.user else ''


def menu_item_converter(menu_item,menu_icons={},use_t=True, default_icon_class=''):
    """Modify menu item for use in MENU helper
    Input menu item format: (label,active,url,submenu) or ((label,iconclass),active,url,submenu)
    Output menu item format: (mod_label,active,url,submenu)
    mod_label format: <i class="fa fa-book"></i><span>label</span>
    """
    if isinstance(menu_item,LI): return menu_item
    if not menu_icons:
        menu_icons=plugins.layout_starter.admin_menu_icons.copy()
        menu_icons.update(plugins.layout_starter.menu_icons)
    if not default_icon_class: default_icon_class=plugins.layout_starter.default_icon_class

    if len(menu_item)==3:
        label,active,url=menu_item
        submenu=[]
    else:
        label,active,url,submenu=menu_item

    if isinstance(label,translator):
        iconclass=default_icon_class
    else:
        iconclass=menu_icons.get(label,default_icon_class)
        label=T(label)
    return (CAT(I(_class=iconclass), SPAN(label)),active,url,[menu_item_converter(x,menu_icons,use_t, default_icon_class) for x in submenu])


def is_user_member(*roles):
    user_auth_groups = [x.lower() for x in auth.user_groups.values()]
    required_auth_groups = [x.lower() for x in roles]
    if auth.user and any(role in required_auth_groups for role in user_auth_groups): return True
    return False


def user_visibility(*groups):
    """in views, in class attribute: =user_visibility('list', 'of', 'authorized', 'user_groups')"""
    return 'hidden' if not is_user_member(*groups) else 'visible'

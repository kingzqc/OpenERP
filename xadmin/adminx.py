from __future__ import absolute_import
import xadmin
from ppm.models import *
from crm.models import *
from base.models import *
from doc.models import *
from psmreport.models import *
from .models import *
# from .models import  UserSettings, Log
from xadmin.layout import *
# zqc test add start -----
from django.shortcuts import render
# zqc test end ---------
from django.utils.translation import ugettext_lazy as _, ugettext
# ZQC add for Q 查询
from django.db.models import Q
from django.db.models import F
# zqc add start for Screen Layout setting ----------------------
from xadmin import views

import xadmin.views
from django import forms, VERSION as django_version
from django.core.exceptions import PermissionDenied
from django.db import router
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from django.contrib.admin.utils import get_deleted_objects
from xadmin.util import model_ngettext
from xadmin.views.base import filter_hook
from django.http import HttpResponse
from import_export import resources
from django.apps import apps

from .forms import *

import json

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from django.core.exceptions import ValidationError

# zqc add for load batch change
BATCH_CHECKBOX_NAME = '_batch_change_fields'

ACTION_CHECKBOX_NAME = '_selected_action'
checkbox = forms.CheckboxInput({'class': 'action-select'}, lambda value: False)

def action_checkbox(obj):
    return checkbox.render(ACTION_CHECKBOX_NAME, force_text(obj.pk))

action_checkbox.short_description = mark_safe(
    '<input type="checkbox" id="action-toggle" />')
action_checkbox.allow_tags = True
action_checkbox.allow_export = False
action_checkbox.is_column = False

# 继承基本动作模板
from xadmin.plugins.actions import BaseActionView
# the following is 自定义action ，比如实现"批准' '指派'等等的操作
class ChangeSelectedAction(BaseActionView):

    action_name = "change_selected"
    description = _(u'Change selected %(verbose_name_plural)s')

    delete_confirmation_template = None
    delete_selected_confirmation_template = None

    delete_models_batch = True

    model_perm = 'change'
    icon = 'fa fa-times'
    username = ' '
    password = ' '

    @filter_hook
    def update_models(self, queryset):
        # 以下 获取模版中的输入内容
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        n = queryset.count()
        if n:
            if self.delete_models_batch:
                self.log('change', _('Batch change %(count)d %(items)s.') % {"count": n, "items": model_ngettext(self.opts, n)})
                queryset.update(Cust_address = username + password)
            else:
                for obj in queryset:
                    self.log('change', '', obj)
                    obj.update()
            self.message_user(_("Successfully changed %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(self.opts, n)
            }, 'success')

    @filter_hook
    def do_action(self, queryset):
        # Check that the user has delete permission for the actual model
        if not self.has_change_permission():
            raise PermissionDenied

        # Populate deletable_objects, a data structure of all related objects that
        # will also be deleted.

        if django_version > (2, 1):
            deletable_objects, model_count, perms_needed, protected = get_deleted_objects(
                queryset, self.opts, self.admin_site)
        else:
            using = router.db_for_write(self.model)
            deletable_objects, model_count, perms_needed, protected = get_deleted_objects(
                queryset, self.opts, self.user, self.admin_site, using)


        # The user has already confirmed the deletion.
        # Do the deletion and return a None to display the change list view again.
        if self.request.POST.get('post'):
            if perms_needed:
                raise PermissionDenied
            self.update_models(queryset)
            # Return None to display the change list page again.
            return None

        if len(queryset) == 1:
            objects_name = force_text(self.opts.verbose_name)
        else:
            objects_name = force_text(self.opts.verbose_name_plural)

        if perms_needed or protected:
            title = _("Cannot change %(name)s") % {"name": objects_name}
        else:
            title = _("Are you sure?")

        context = self.get_context()
        context.update({
            "title": title,
            "objects_name": objects_name,
            "deletable_objects": [deletable_objects],
            'queryset': queryset,
            "perms_lacking": perms_needed,
            "protected": protected,
            "opts": self.opts,
            "app_label": self.app_label,
            'action_checkbox_name': ACTION_CHECKBOX_NAME,
        })

        # Display the confirmation page
        return TemplateResponse(self.request, self.delete_selected_confirmation_template or
                                self.get_template_list('views/model_change_selected_confirm.html'), context)

# the above is 自定义action ，比如实现"批准' '指派'等等的操作

class BaseSetting(object):
    #    """xadmin的基本配置"""
    enable_language = True #开启切换语言
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True  # 支持切换主题

xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    # PSM add  Header and Footer -------
    site_header = 'PSM系统'
    site_title = "---PSM系统 V1.0"
    site_footer = "Professional Service Management System @2022"
    menu_style = "accordion"

# PSM  自定义快捷菜单设置
    def get_site_menu(self):

        return (
       )
#注册你上面填写的url
from xadmin.views import CommAdminView
xadmin.site.register(views.CommAdminView, GlobalSetting)
# zqc add end ---------------------------------------------

class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = False

xadmin.site.register(UserSettings, UserSettingsAdmin)


class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url(
                '%s_%s_change' % (instance.content_type.app_label, instance.content_type.model),
                instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''

    link.short_description = ""
    link.allow_tags = True
    link.is_column = False

    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'
    # zqc add for menu hide ---------------
    hidden_menu = False

xadmin.site.register(Log, LogAdmin)

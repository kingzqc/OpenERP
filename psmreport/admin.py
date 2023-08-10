
import xadmin
from crm.models import *
from base.models import *
from psmreport.models import *
from xadmin.layout import *
from django.forms.widgets import *
from django.contrib.admin.widgets import *
from django.utils.html import format_html
from django.http import HttpResponse
from django.core.validators import *
from django.core.validators import ValidationError
from django.contrib import messages
from django.shortcuts import render,redirect
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from xadmin.views import CommAdminView

# Register your models here.
class Psm_dashboardAdmin(object):
    object_list_template = 'psm_dashboard.html'
    print(object)
    def get_context(self):
        context = CommAdminView.get_context(self)

        bill_message = AccountMaster.objects.all()
        context.update(
            {
                'title': 'PSM数据分析仪表版',
                'bill_message': bill_message,
            }
        )

        return context
xadmin.site.register(psm_dashboard, Psm_dashboardAdmin)
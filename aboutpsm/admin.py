
import xadmin
from crm.models import *
from ppm.models import *
from base.models import *
from aboutpsm.models import *
from xadmin.views import CommAdminView
from xadmin.views.base import get_account_bu  # psm add for get BU
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from aboutpsm.views import *
# Register your models here.
# myself 我的工作日历 appointment
class Psm_myselfAdmin(object):
    model_icon = 'fa fa-calendar-o'
    object_list_template = 'mycalendar.html'

xadmin.site.register(psm_myself, Psm_myselfAdmin)
# psm funnel 商机漏斗
class Psm_funnelAdmin(object):
    model_icon = 'fa fa-users'
    object_list_template = 'psm_funnel.html'

    def get_context(self):
        context = CommAdminView.get_context(self)

        bill_message = UserProfile.objects.all()
        context.update(
            {
                'title': '团队数据分析',
                'bill_message': bill_message,
            }
        )

        return context
xadmin.site.register(psm_funnel, Psm_funnelAdmin)

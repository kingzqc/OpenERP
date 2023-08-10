
from django.apps import AppConfig
from django.core import checks
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

class CrmConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'crm'
    verbose_name = _("客户管理")
    app_icon = 'fa fa-heart'
    orderIndex = 3
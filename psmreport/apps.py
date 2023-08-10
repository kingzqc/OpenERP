from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class PsmreportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'psmreport'
    verbose_name = _("PSM数据分析")
    app_icon = 'fa fa-folder'
    orderIndex = 1
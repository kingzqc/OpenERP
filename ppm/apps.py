from django.apps import AppConfig
from django.core import checks
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _


class PpmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ppm'
    verbose_name = _("项目合同管理")
    app_icon = 'fa fa-folder'
    orderIndex = 5
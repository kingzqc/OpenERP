
from django.apps import AppConfig
from django.core import checks
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
    verbose_name = _("基础参数")
    app_icon = 'fa fa-folder'
    orderIndex = 2
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DocConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'doc'
    verbose_name = _('Web内容管理')
    app_icon = 'fa fa-folder'
    orderIndex = 6
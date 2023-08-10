from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
#
class WorkflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workflow'
    verbose_name = _("工作流程管理")
    app_icon = 'fa fa-folder'
    orderIndex = 4
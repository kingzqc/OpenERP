from django.apps import AppConfig
from django.core import checks
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

import xadmin


class XAdminConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""
    app_icon = 'fa fa-star'
    name = 'xadmin'
    verbose_name = _("用户自定义")
    orderIndex = 1

    def ready(self):
        self.module.autodiscover()
        setattr(xadmin,'site',xadmin.site)

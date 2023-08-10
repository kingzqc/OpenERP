from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AboutpsmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aboutpsm'
    verbose_name = _("关于我")
    app_icon = 'fa fa-star'
    orderIndex = 0
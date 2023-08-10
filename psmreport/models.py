from django.db import models
from django.contrib import admin

from django.utils.html import format_html
from django.core.validators import *
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import ValidationError
from django.utils.safestring import mark_safe

# Create your models here.
# 自定义页面实现自己要的功能，不遵循XADMIN模板
class psm_dashboard(models.Model):

    class Meta:
        verbose_name = u"仪表板"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Meta.verbose_name
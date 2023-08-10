from django.db import models
from django.contrib import admin

from django.utils.html import format_html
from django.core.validators import *
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import ValidationError
from django.utils.safestring import mark_safe

# Create your models here.
#  所有choices 参数来自于 psmsetting.py  =====

# 自定义页面实现自己要的功能，不遵循XADMIN模板
class psm_myself(models.Model):

    class Meta:
        verbose_name = u"我的日程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Meta.verbose_name
class psm_funnel(models.Model):

    class Meta:
        verbose_name = u"商机漏斗"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Meta.verbose_name

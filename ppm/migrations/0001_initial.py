# Generated by Django 2.2.26 on 2023-05-25 09:34

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doc', '0001_initial'),
        ('base', '0002_auto_20230525_1734'),
        ('crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractMaster',
            fields=[
                ('Data_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('Contract_code', models.CharField(max_length=20, verbose_name='合同代码')),
                ('Contract_name', models.CharField(max_length=200, verbose_name='合同名称')),
                ('Contract_method', models.CharField(choices=[('EMAIL', '电子邮件'), ('CALL', '电话'), ('WECHAT', '微信')], max_length=10, verbose_name='合同方式')),
                ('Contract_content', models.TextField(blank=True, null=True, verbose_name='合同内容')),
                ('Contract_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='合同标的')),
                ('Contract_finishamount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='完成金额')),
                ('Contract_updatedate', models.DateField(blank=True, null=True, verbose_name='更新日期')),
                ('Contract_startdate', models.DateField(blank=True, null=True, verbose_name='开始日期')),
                ('Contract_enddate', models.DateField(blank=True, null=True, verbose_name='结束日期')),
                ('Contract_nowstage', models.CharField(blank=True, max_length=20, null=True, verbose_name='当前进展')),
                ('Contract_nextstage', models.CharField(blank=True, max_length=20, null=True, verbose_name='接续目标')),
                ('Contract_status', models.CharField(default='OK', max_length=2, validators=[django.core.validators.MinLengthValidator(1, message='20警示：')], verbose_name='状态')),
                ('Contract_comment', models.TextField(blank=True, null=True, verbose_name='合同备注')),
                ('Data_security', models.CharField(choices=[('10', '10'), ('30', '30'), ('50', '50'), ('100', '100')], max_length=10, verbose_name='权限级别')),
                ('Contract_initdate', models.DateField(blank=True, null=True, verbose_name='建立日期')),
                ('Contract_changedate', models.DateField(blank=True, null=True, verbose_name='修改日期')),
                ('Dummy_id', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='流水号')),
            ],
            options={
                'verbose_name': '合同',
                'verbose_name_plural': '合同',
            },
        ),
        migrations.CreateModel(
            name='ContractResourceMaster',
            fields=[
                ('Data_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('ContractResource_name', models.CharField(max_length=20, verbose_name='合同名称')),
                ('ContractResource_role', models.CharField(choices=[('PM', '项目经理'), ('SM', '高级成员'), ('NM', '普通成员')], max_length=12, verbose_name='角色')),
                ('ContractResource_member', models.CharField(max_length=20, verbose_name='资源')),
                ('ContractResource_type', models.CharField(choices=[('LB', '人工工时'), ('IT', '物品'), ('OT', '其它')], max_length=10, verbose_name='资源类型')),
                ('ContractResource_unit', models.CharField(choices=[('HR', '小时'), ('PC', '件'), ('EA', '个')], max_length=10, verbose_name='资源单位')),
                ('ContractResource_quantity', models.IntegerField(default=0, verbose_name='数量')),
                ('ContractResource_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='金额')),
                ('ContractResource_status', models.CharField(default='OK', max_length=2, validators=[django.core.validators.MinLengthValidator(1, message='20警示：')], verbose_name='状态')),
                ('ContractResource_comment', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('Data_security', models.CharField(choices=[('10', '10'), ('30', '30'), ('50', '50'), ('100', '100')], max_length=10, verbose_name='权限级别')),
            ],
            options={
                'verbose_name': '合同资源',
                'verbose_name_plural': '合同资源',
            },
        ),
        migrations.CreateModel(
            name='ProjectMaster',
            fields=[
                ('Data_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('Project_code', models.CharField(max_length=20, verbose_name='项目代码')),
                ('Project_name', models.CharField(max_length=200, verbose_name='项目名称')),
                ('Project_method', models.CharField(choices=[('EMAIL', '电子邮件'), ('CALL', '电话'), ('WECHAT', '微信')], max_length=12, verbose_name='项目方式')),
                ('Project_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='金额')),
                ('Project_quantity', models.DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name='服务数量')),
                ('Project_days', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='工作天数')),
                ('Project_realizeamount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='已实现金额')),
                ('Project_processamount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='已处理金额')),
                ('Project_realizeqty', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='已实现数量')),
                ('Project_realizedays', models.DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name='已实现天数')),
                ('Project_processqty', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='已处理数量')),
                ('Project_prcessdays', models.DecimalField(decimal_places=1, default=0.0, max_digits=10, verbose_name='已处理天数')),
                ('Project_updatedate', models.DateField(blank=True, null=True, verbose_name='更新日期')),
                ('Project_startdate', models.DateField(blank=True, null=True, verbose_name='开始日期')),
                ('Project_enddate', models.DateField(blank=True, null=True, verbose_name='结束日期')),
                ('Project_nowstage', models.CharField(blank=True, max_length=20, null=True, verbose_name='当前进展')),
                ('Project_nextstage', models.CharField(blank=True, max_length=20, null=True, verbose_name='接续目标')),
                ('Project_comment', models.TextField(blank=True, max_length=800, null=True, verbose_name='备注')),
                ('Data_security', models.CharField(choices=[('10', '10'), ('30', '30'), ('50', '50'), ('100', '100')], max_length=10, verbose_name='权限级别')),
                ('Data_datetime', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='日期')),
                ('Project_status', models.CharField(choices=[('OO', '待办'), ('OK', '启用'), ('XX', '停止')], default='  ', max_length=2, validators=[django.core.validators.MinLengthValidator(1, message='20警示：')], verbose_name='状态')),
                ('Dummy_id', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='流水号')),
                ('Data_bu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Data_bucprj', to='base.BUMaster', to_field='BU_code', verbose_name='所属BU')),
                ('Data_creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Prj_userdc', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('Data_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Prj_userdo', to=settings.AUTH_USER_MODEL, verbose_name='拥有者')),
                ('Data_secondowner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Prj_userds', to=settings.AUTH_USER_MODEL, verbose_name='第二拥有者')),
                ('Project_customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prj_cust1', to='crm.CustomerMaster', verbose_name='客户')),
                ('Project_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prj_doc1', to='doc.DocumentMaster', verbose_name='相关文档')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
            },
        ),
        migrations.CreateModel(
            name='ProjectResourceMaster',
            fields=[
                ('Data_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('ProjectResource_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='项目资源名称')),
                ('ProjectResource_role', models.CharField(blank=True, choices=[('PM', '项目经理'), ('SM', '高级成员'), ('NM', '普通成员')], max_length=12, null=True, verbose_name='角色')),
                ('ProjectResource_type', models.CharField(blank=True, choices=[('LB', '人工工时'), ('IT', '物品'), ('OT', '其它')], max_length=10, null=True, verbose_name='资源类型')),
                ('ProjectResource_unit', models.CharField(blank=True, choices=[('HR', '小时'), ('PC', '件'), ('EA', '个')], default='EA', max_length=10, null=True, verbose_name='资源单位')),
                ('ProjectResource_quantity', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='数量')),
                ('ProjectResource_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True, verbose_name='金额')),
                ('ProjectResource_status', models.CharField(default='OK', max_length=2, validators=[django.core.validators.MinLengthValidator(1, message='20警示：')], verbose_name='状态')),
                ('ProjectResource_comment', models.TextField(blank=True, max_length=800, null=True, verbose_name='备注')),
                ('Data_security', models.CharField(choices=[('10', '10'), ('30', '30'), ('50', '50'), ('100', '100')], max_length=10, verbose_name='权限级别')),
                ('Data_datetime', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='日期')),
                ('Data_bu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Data_bucpr', to='base.BUMaster', to_field='BU_code', verbose_name='所属BU')),
                ('Data_creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Prjr_usersc', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('Data_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Prjr_userso', to=settings.AUTH_USER_MODEL, verbose_name='拥有者')),
                ('ProjectResource_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Prjr_usermbr', to=settings.AUTH_USER_MODEL, verbose_name='成员')),
                ('ProjectResource_serviceitem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Item_codepr', to='base.ItemMaster', verbose_name='服务内容')),
                ('Project_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prj_code1', to='ppm.ProjectMaster', verbose_name='项目代码')),
            ],
            options={
                'verbose_name': '项目资源',
                'verbose_name_plural': '项目资源',
            },
        ),
    ]

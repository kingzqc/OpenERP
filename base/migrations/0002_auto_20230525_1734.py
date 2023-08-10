# Generated by Django 2.2.26 on 2023-05-25 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doc', '0001_initial'),
        ('base', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='userthumbup',
            name='Job_thumbup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Job_thumbup', to='doc.JobMaster', to_field='Dummy_id', verbose_name='Job点赞'),
        ),
        migrations.AddField(
            model_name='userthumbup',
            name='User_myself',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_myself0', to=settings.AUTH_USER_MODEL, to_field='Dummy_id', verbose_name='关注人'),
        ),
        migrations.AddField(
            model_name='userthumbup',
            name='User_thumbup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_thumbup', to='doc.ResourceMaster', to_field='Dummy_id', verbose_name='资源点赞'),
        ),
        migrations.AddField(
            model_name='userinterest',
            name='User_interest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_interest', to='doc.ResourceMaster', to_field='Dummy_id', verbose_name='关注对象'),
        ),
        migrations.AddField(
            model_name='userinterest',
            name='User_myself',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_myself', to=settings.AUTH_USER_MODEL, to_field='Dummy_id', verbose_name='关注人'),
        ),
        migrations.AddField(
            model_name='itemmaster',
            name='Data_bu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BU_namesi', to='base.BUMaster', to_field='BU_code', verbose_name='所属BU'),
        ),
        migrations.AddField(
            model_name='itemmaster',
            name='Data_creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Req_userim', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='buparameter',
            name='Bu_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BU_name1', to='base.BUMaster', to_field='BU_code', verbose_name='所属BU'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Data_bu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BU_codeu', to='base.BUMaster', to_field='BU_code', verbose_name='所属BU'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='defaultresource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dft_resource', to='doc.ResourceMaster', verbose_name='默认资源'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_manager', to=settings.AUTH_USER_MODEL, verbose_name='上级'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='resourcetype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Content_type0', to='doc.ContentType', verbose_name='资源类型'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='userthumbup',
            unique_together={('User_myself', 'User_thumbup', 'Job_thumbup')},
        ),
        migrations.AlterUniqueTogether(
            name='userinterest',
            unique_together={('User_myself', 'User_interest')},
        ),
        migrations.AlterUniqueTogether(
            name='itemmaster',
            unique_together={('Data_bu', 'Item_code')},
        ),
        migrations.AlterUniqueTogether(
            name='buparameter',
            unique_together={('Bu_code', 'Bu_paratype', 'Bu_parakey')},
        ),
    ]

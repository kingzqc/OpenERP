# Generated by Django 2.2.26 on 2023-03-16 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='psm_dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '仪表板',
                'verbose_name_plural': '仪表板',
            },
        ),
    ]

# Generated by Django 3.2.9 on 2022-10-12 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_auto_20190326_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acmcontestrank',
            name='submission_info',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='contest',
            name='allowed_ip_ranges',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='oicontestrank',
            name='submission_info',
            field=models.JSONField(default=dict),
        ),
    ]

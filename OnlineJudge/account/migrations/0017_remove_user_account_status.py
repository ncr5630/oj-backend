# Generated by Django 3.2.9 on 2022-10-14 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_alter_user_account_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='account_status',
        ),
    ]

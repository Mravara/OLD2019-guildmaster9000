# Generated by Django 3.0.1 on 2019-12-26 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raid', '0009_remove_raidmember_raid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raidmember',
            name='name',
        ),
    ]

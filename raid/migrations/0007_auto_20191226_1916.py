# Generated by Django 3.0.1 on 2019-12-26 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_member_ep'),
        ('raid', '0006_auto_20191226_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raid',
            name='raid_members',
            field=models.ManyToManyField(to='members.Member'),
        ),
    ]

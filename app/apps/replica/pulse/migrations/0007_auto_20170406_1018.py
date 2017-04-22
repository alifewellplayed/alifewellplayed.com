# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-06 10:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import replica.pulse.models


class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0006_sitesettings_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='page',
            field=models.ForeignKey(blank=True, default=replica.pulse.models.DefaultEntry, null=True, on_delete=django.db.models.deletion.CASCADE, to='pulse.Entry'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='url',
            field=models.URLField(blank=True, max_length=510),
        ),
    ]
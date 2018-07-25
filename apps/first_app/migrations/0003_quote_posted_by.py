# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-24 00:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='posted_by',
            field=models.ForeignKey(default=17, on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='first_app.User'),
            preserve_default=False,
        ),
    ]
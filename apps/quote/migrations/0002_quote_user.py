# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 18:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_quote', to='quote.User'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-23 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0002_auto_20180323_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faves',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Quotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.CharField(max_length=255)),
                ('quoter', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted', to='belt.Users')),
            ],
            managers=[
                ('quotes', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='faves',
            name='favequote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favequote', to='belt.Quotes'),
        ),
        migrations.AddField(
            model_name='faves',
            name='userfave',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userfave', to='belt.Users'),
        ),
    ]

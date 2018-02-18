# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-18 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='Code')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('type', models.CharField(choices=[('01', 'PRODUCT'), ('02', 'SERVICE')], default='01', max_length=2, verbose_name='Type')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='Code')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Image')),
                ('score', models.DecimalField(decimal_places=2, default=0.0, max_digits=3, verbose_name='Score')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Price')),
                ('provider_id', models.CharField(max_length=40, verbose_name='Provider')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catalog.Category')),
            ],
            options={
                'verbose_name_plural': 'Items',
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'db_table': 'tag',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(to='catalog.Tag'),
        ),
    ]

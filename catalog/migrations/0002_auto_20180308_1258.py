# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-08 17:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('provider', models.CharField(max_length=50, verbose_name='Name')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name_plural': 'Catalogs',
                'db_table': 'catalog',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Price')),
                ('reference_price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Reference Price')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Discount')),
                ('threshold', models.PositiveIntegerField(default=100, verbose_name='threshold')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='catalog.Catalog')),
                ('tags', models.ManyToManyField(to='catalog.Tag')),
            ],
            options={
                'verbose_name_plural': 'Offers',
                'db_table': 'offer',
            },
        ),
        migrations.CreateModel(
            name='OfferItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('01', 'PRODUCT'), ('02', 'SERVICE')], default='01', max_length=2, verbose_name='Type')),
                ('item', models.CharField(max_length=50, verbose_name='Item')),
                ('count', models.PositiveIntegerField(default=1, verbose_name='Count')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catalog.Offer')),
            ],
            options={
                'verbose_name_plural': 'OfferItems',
                'db_table': 'offer_item',
            },
        ),
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.RemoveField(
            model_name='item',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='category',
            name='type',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.AddField(
            model_name='catalog',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalogs', to='catalog.Category'),
        ),
    ]

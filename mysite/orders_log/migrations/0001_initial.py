# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('content', models.TextField()),
                ('published', models.DateTimeField()),
                ('last_edited', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('url', models.CharField(blank=True, max_length=250)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('shipped', models.DateTimeField(null=True, blank=True)),
                ('received', models.DateTimeField(null=True, blank=True)),
                ('shippingDateTo', models.DateTimeField(null=True, blank=True)),
                ('shippingDateFrom', models.DateTimeField(null=True, blank=True)),
                ('shippingDaysTo', models.IntegerField(null=True, blank=True)),
                ('shippingDaysFrom', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('ordered', models.DateTimeField()),
                ('shipped', models.DateTimeField(null=True, blank=True)),
                ('received', models.DateTimeField(null=True, blank=True)),
                ('shippingDateTo', models.DateTimeField(null=True, blank=True)),
                ('shippingDateFrom', models.DateTimeField(null=True, blank=True)),
                ('shippingDaysTo', models.IntegerField(null=True, blank=True)),
                ('shippingDaysFrom', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('homepage', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(null=True, to='orders_log.Store', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.ForeignKey(to='orders_log.Order'),
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(null=True, to='orders_log.Item', blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='order',
            field=models.ForeignKey(null=True, to='orders_log.Order', blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='store',
            field=models.ForeignKey(null=True, to='orders_log.Store', blank=True),
        ),
    ]

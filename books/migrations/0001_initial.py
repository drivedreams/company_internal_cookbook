# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Custom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('sex', models.CharField(max_length=1, choices=[('M', '男'), ('F', '女')], verbose_name='性别')),
                ('age', models.IntegerField()),
                ('pic', models.ImageField(upload_to='upload/images/custom', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FormCustoms',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('custom', models.ForeignKey(to='books.Custom')),
            ],
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('description', models.CharField(max_length=200, blank=True, null=True)),
                ('times', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('pic', models.ImageField(upload_to='upload/images/good_pic', default='')),
                ('category', models.ForeignKey(to='books.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('remark', models.CharField(max_length=200, blank=True, default='')),
                ('comment', models.CharField(max_length=200, blank=True, default='')),
                ('score', models.IntegerField(default=0)),
                ('custom', models.ForeignKey(to='books.Custom')),
                ('good', models.ForeignKey(to='books.Good')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, default='晚餐')),
                ('date', models.DateTimeField(default='')),
                ('state', models.IntegerField(choices=[(1, '开启'), (2, '关闭')], default=1, verbose_name='订单状态')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('URL', models.CharField(max_length=200, default='')),
                ('pic', models.ImageField(upload_to='upload/images/good_pic', default='')),
            ],
        ),
        migrations.CreateModel(
            name='SignUpForm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
                ('state', models.IntegerField(choices=[(1, '开启'), (2, '关闭')], default=1, verbose_name='报名表状态')),
                ('order', models.ForeignKey(blank=True, to='books.Order', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(to='books.Restaurant'),
        ),
        migrations.AddField(
            model_name='menu',
            name='order',
            field=models.ForeignKey(to='books.Order'),
        ),
        migrations.AddField(
            model_name='good',
            name='restaurant',
            field=models.ForeignKey(to='books.Restaurant'),
        ),
        migrations.AddField(
            model_name='formcustoms',
            name='sign_up_form',
            field=models.ForeignKey(to='books.SignUpForm'),
        ),
        migrations.AddField(
            model_name='custom',
            name='department',
            field=models.ForeignKey(to='books.Department'),
        ),
        migrations.AddField(
            model_name='custom',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

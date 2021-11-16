# Generated by Django 3.2.9 on 2021-11-16 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20211115_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IPアドレス')),
                ('name', models.CharField(max_length=32, verbose_name='名前')),
                ('contents', models.CharField(max_length=255, verbose_name='内容')),
                ('is_active', models.BooleanField(default=True, verbose_name='有効フラグ')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
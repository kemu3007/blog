# Generated by Django 3.2.9 on 2021-11-16 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20211117_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
        ),
    ]

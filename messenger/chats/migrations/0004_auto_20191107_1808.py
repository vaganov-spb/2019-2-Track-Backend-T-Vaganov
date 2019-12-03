# Generated by Django 2.2.5 on 2019-11-07 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_auto_20191105_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='type',
            field=models.CharField(max_length=10, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='url',
            field=models.URLField(verbose_name='Адрес изображения'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='last_message',
            field=models.CharField(max_length=4096, verbose_name='Последнне прочитанное сообщение'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='topic',
            field=models.CharField(max_length=32, verbose_name='Название чата'),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.CharField(max_length=4096, verbose_name='Содержание'),
        ),
    ]

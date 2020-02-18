# Generated by Django 2.2.5 on 2019-12-03 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0005_auto_20191113_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='name',
            field=models.CharField(default='qwee', max_length=100, verbose_name='Имя файла'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attachment',
            name='url',
            field=models.FileField(max_length=200, upload_to='media/', verbose_name='Файл'),
        ),
    ]

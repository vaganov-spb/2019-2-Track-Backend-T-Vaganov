# Generated by Django 2.2.5 on 2019-11-05 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_auto_20191102_0829'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachment',
            options={'verbose_name': 'Вложение', 'verbose_name_plural': 'Вложения'},
        ),
        migrations.AlterModelOptions(
            name='chat',
            options={'verbose_name': 'Чат', 'verbose_name_plural': 'Чаты'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-added_at'], 'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
    ]

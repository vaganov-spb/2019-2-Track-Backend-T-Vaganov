# Generated by Django 2.2.5 on 2019-12-10 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0009_auto_20191210_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='added_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Time and Date of sending'),
        ),
    ]
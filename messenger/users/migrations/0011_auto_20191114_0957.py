# Generated by Django 2.2.5 on 2019-11-14 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20191113_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='new_messages',
            field=models.BooleanField(default=False),
        ),
    ]

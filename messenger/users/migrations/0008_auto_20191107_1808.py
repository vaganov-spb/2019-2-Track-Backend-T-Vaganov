# Generated by Django 2.2.5 on 2019-11-07 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20191106_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nick',
            field=models.CharField(max_length=16, unique=True, verbose_name='Никнейм'),
        ),
    ]

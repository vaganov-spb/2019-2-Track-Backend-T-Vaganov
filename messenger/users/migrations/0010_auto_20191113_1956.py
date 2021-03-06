# Generated by Django 2.2.5 on 2019-11-13 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_user_nick'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.Chat', verbose_name='chat_id'),
        ),
        migrations.AlterField(
            model_name='member',
            name='last_read_message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='chats.Message', verbose_name='last read message id'),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id'),
        ),
    ]

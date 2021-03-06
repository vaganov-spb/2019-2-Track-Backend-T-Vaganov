# Generated by Django 2.2.5 on 2019-11-01 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_user_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_group_chat', models.BooleanField(default=False)),
                ('topic', models.CharField(max_length=32)),
                ('last_message', models.CharField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=4096)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Time and Date of sending')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.Chat', verbose_name='chat id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='user id')),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('url', models.CharField(max_length=150)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.Chat', verbose_name='chat id')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.Message', verbose_name='message id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User', verbose_name='user id')),
            ],
        ),
    ]

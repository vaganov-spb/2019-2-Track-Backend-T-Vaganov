from django.db import models
from users.models import User
from datetime import datetime

class Chat(models.Model):
    is_group_chat = models.BooleanField(default=False)
    topic = models.CharField(
        max_length=32,
        blank=False,
        verbose_name='Название чата',
    )
    last_message = models.CharField(
        max_length=4096,
        blank=False,
        null=True,
        verbose_name='Последнне прочитанное сообщение',
    )

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="chat id",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="user id",
    )
    content = models.CharField(
        max_length=4096,
        blank=False,
        verbose_name='Содержание',
    )
    added_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Time and Date of sending",
    )

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-added_at']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Attachment(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        verbose_name="chat id",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="user id",
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="message id",
    )

    type = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='Тип',
    )

    name = models.CharField(
        blank=False,
        max_length=100,
        null=False,
        verbose_name='Имя файла',
    )

    file = models.FileField(
        max_length=200,
        blank=False,
        upload_to='media/',
        verbose_name='Файл',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'


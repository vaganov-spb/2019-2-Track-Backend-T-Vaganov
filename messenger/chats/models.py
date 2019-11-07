from django.db import models
from users.models import User

class Chat(models.Model):
    is_group_chat = models.BooleanField(default=False)
    topic = models.CharField(
        max_length=32,
        blank=False,
    )
    last_message = models.CharField(
        max_length=4096,
        blank=False
    )

    def __str__(self):
        return self.last_message

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

class Message(models.Model):
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
    content = models.CharField(
        max_length=4096,
        blank=False,
    )
    added_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
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
        max_length=10,
        blank=False,
    )
    url = models.URLField(
        max_length=200,
        blank=False,
    )

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'


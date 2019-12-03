from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatar/',
        blank=True,
        null=True,
        verbose_name='Аватар',
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи' 


class Member(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="user_id",
    )
    chat = models.ForeignKey(
        'chats.Chat',
        on_delete=models.CASCADE,
        verbose_name="chat_id",
    )

    new_messages = models.BooleanField(default=False)

    last_read_message = models.ForeignKey(
        'chats.Message',
        null=True,
        on_delete=models.PROTECT,
        verbose_name="last read message id",
    )

    def __str__(self):
        return f'{self.user.__str__()} in {self.chat.__str__()}'

    class Meta:
        verbose_name = 'Участник чата'
        verbose_name_plural = 'Участники чата'



from chats.views import chat_list, particular_chat
from django.urls import path, re_path

urlpatterns = [
    path('<int:user_id>/', chat_list, name='chat_list'),
    path('<int:user_id>/<int:chat_id>', particular_chat, name='particular_chat'),
]

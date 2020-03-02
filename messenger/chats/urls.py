from chats.views import chats, create_chat, send_message, particular_chat, read_mess, attachment_save, get_attachment
from django.urls import path, re_path

urlpatterns = [
    #path('<int:user_id>/', chat_list, name='chat_list'),
    path('<int:user_id>/newchat/', create_chat, name='createChat'),
    path('<int:user_id>/', chats, name='chats'),
    path('<int:user_id>/newmessage/', send_message, name='send_message'),
    path('<int:user_id>/<int:chat_id>/readmess/', read_mess, name='read_mess'),
    path('<int:user_id>/<int:chat_id>/', particular_chat, name='particular_chat'),
    path('attachment/', attachment_save, name='attachment_save'),
    path('<int:user_id>/attachment/<int:attachment_id>', get_attachment, name='get_attachment'),
]
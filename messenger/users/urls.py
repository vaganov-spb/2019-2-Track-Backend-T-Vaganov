from users.views import profile, contact_list, search_by_username
from chats.views import chats, create_chat, message_list
from django.urls import path, re_path

# /users/?search=root
# /users/12/
urlpatterns = [
    path('', search_by_username, name='search_by_username'),
    path('<int:user_id>/messages/', message_list, name='message_list'),
    path('<int:user_id>/', profile, name='profile'),
    path('<int:user_id>/contacts/', contact_list, name='contact_list'),
]
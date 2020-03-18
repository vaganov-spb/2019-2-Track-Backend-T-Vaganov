from users.views import profile, contact_list, search_by_username
from chats.views import chats, create_chat, message_list
from django.urls import path, re_path, include
from users import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'url', views.GetMembers, basename='GetMembers')
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', search_by_username, name='search_by_username'),
    path('rest/', include(router.urls)),
    # path('auth/', get_id, name='get_id'),
    path('<int:user_id>/messages/', message_list, name='message_list'),
    path('<int:user_id>/', profile, name='profile'),
    path('<int:user_id>/contacts/', contact_list, name='contact_list'),
]
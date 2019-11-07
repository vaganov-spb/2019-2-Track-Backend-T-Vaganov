from users.views import profile, contact_list
from django.urls import path, re_path

urlpatterns = [
    path('<int:user_id>/', profile, name='profile'),
    path('<int:user_id>/contacts/', contact_list, name='contact_list'),
]
from home.views import enterpage
from django.urls import path, re_path

urlpatterns = [
    path('', enterpage, name='enterpage'),
]
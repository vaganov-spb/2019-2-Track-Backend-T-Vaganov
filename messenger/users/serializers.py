from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "last_login", "username", "first_name", "last_name", "avatar"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "last_login", "username", "first_name", "last_name", "avatar", "date_joined"]

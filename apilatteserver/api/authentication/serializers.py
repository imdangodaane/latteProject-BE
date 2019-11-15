from rest_framework import serializers
from .models import Login

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['userid', 'user_pass']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['userid', 'user_pass', 'email', 'sex', 'birthdate']
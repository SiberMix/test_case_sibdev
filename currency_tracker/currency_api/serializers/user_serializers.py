from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Схема для регистрации пользователя
    """
    password = serializers.CharField(
        write_only=True,
        help_text="Пароль пользователя."
    )
    email = serializers.EmailField(
        help_text="Почтовый адрес пользователя."
    )
    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['email']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Авторизация
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Unable to log in with provided credentials.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        refresh = RefreshToken.for_user(user)
        data['user'] = user
        data['access_token'] = str(refresh.access_token)

        return data
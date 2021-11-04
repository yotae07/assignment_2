from rest_framework import serializers
from apps.users.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=190, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=100)
    role = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role']

    def validate_role(self, value):
        if value not in [User.ADMIN, User.GENERAL]:
            raise

        return value

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance

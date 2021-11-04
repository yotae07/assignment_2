from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import permissions
from .serializers import UserSerializer
from apps.users.models import User


class UserViewSet(CreateModelMixin,
                  GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

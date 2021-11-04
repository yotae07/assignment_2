from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.accounts.views import UserViewSet
from api.products.views import ProductViewSet, ItemViewSet, TagViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('user', UserViewSet, basename='user')
router.register('product', ProductViewSet, basename='product')
product = NestedSimpleRouter(router, 'product', lookup='product')
product.register('item', ItemViewSet, basename='item')
product.register('tag', TagViewSet, basename='tag')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', include(product.urls)),
]

from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rareapi.views import register_user, login_user, PostViewSet, TagViewSet, CategoryViewSet

"""Router"""
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet, 'post')
router.register(r'tags', TagViewSet, 'tag')
router.register(r'categories', CategoryViewSet, 'category')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]


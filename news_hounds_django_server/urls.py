from rareapi.views.Subscriptions import SubscriptionsViewSet
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rareapi.views import register_user, login_user, PostViewSet, TagViewSet, CategoryViewSet, CommentViewSet, PostTagsViewSet, ProfileViewSet
from django.conf.urls.static import static
from django.conf import settings


"""Router"""
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet, 'post')
router.register(r'tags', TagViewSet, 'tag')
router.register(r'comments', CommentViewSet, 'comment')
router.register(r'posttags', PostTagsViewSet, 'posttags' )
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'subscriptions', SubscriptionsViewSet, 'subscription')
router.register(r'profiles', ProfileViewSet, 'profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


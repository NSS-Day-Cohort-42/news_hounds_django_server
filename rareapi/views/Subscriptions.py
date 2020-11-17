""" View Module FOr handling requests about subscriptions"""
from django.http.response import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.utils import timezone
from rareapi.models import RareUsers, Subscriptions

#Define a Subscriptions Class
class SubscriptionsViewSet(ViewSet):
    def create(self, request):
        author_id = request.data["author_id"]
        djangoUser = request.auth.user
        follower = RareUsers.objects.get(user=djangoUser)
        try:
            author = RareUsers.objects.get(pk=author_id)
        except RareUsers.DoesNotExist:
            return Response({'message': 'Author does not exist'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if follower == author:
            return Response({'message': 'User can\'t subscribe to themself'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            subscription = Subscriptions.objects.get(follower=follower, author=author, ended_on=None)
            return Response({'message': 'Subscription already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Subscriptions.DoesNotExist:
            subscription = Subscriptions()
            subscription.follower = follower
            subscription.author= author
            subscription.created_on = timezone.now()
            subscription.ended_on = None
        try:
            subscription.save()
            return Response({}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" View Module FOr handling requests about subscriptions"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.utils import timezone
from rareapi.models import RareUsers, Subscriptions


class SubscriptionsViewSet(ViewSet):
    def create(self, request):
        """Handle POST operation"""
        author_id = request.data["author_id"]
        djangoUser = request.auth.user
        follower = RareUsers.objects.get(user=djangoUser)
        #Check the request to make sure the user they are trying to subscribe to exists
        try:
            author = RareUsers.objects.get(pk=author_id)
        except RareUsers.DoesNotExist:
            return Response({'message': 'Author does not exist'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        #Check the request to make sure the request isn't trying to subscribe a rareUser to themself
        if follower == author:
            return Response({'message': 'User can\'t subscribe to themself'}, status=status.HTTP_400_BAD_REQUEST)
        #Check the request to make sure the request isn't duplicating an already existing subscription
        try:
            subscription = Subscriptions.objects.get(follower=follower, author=author, ended_on=None)
            return Response({'message': 'Subscription already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Subscriptions.DoesNotExist:
        #Build the subscription instance based off the model, set the values and then save it to the dataBase
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
    """action to update the ended_on date for when someone unsubscribes"""
    @action(methods=['put'], detail=False)
    def end_subscription(self,request):
        #First gather all the data needed from the request
        author_id = request.data["author_id"]
        #This is the author
        author = RareUsers.objects.get(pk=author_id)
        django_user = request.auth.user
        #This is the follower (the person logged in and Unsubscribing)
        follower = RareUsers.objects.get(user=django_user)
        #Next get the subscriptions
        subscription=Subscriptions.objects.get(author=author, follower=follower,ended_on=None)
        #Finally add the ended on time at the time of request
        subscription.ended_on = timezone.now()
        try:
            subscription.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



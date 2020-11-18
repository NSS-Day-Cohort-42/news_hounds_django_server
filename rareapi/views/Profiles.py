from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rareapi.models import RareUsers
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.http.response import HttpResponseServerError

class ProfileViewSet(ViewSet):
    def list(self, request):
        users = RareUsers.objects.all()
        serializer = BasicProfileSerializer(users, many=True, context={'request':request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET request for single profile
        Returns:
            Response JSON serielized profile instance
        """
        try:
            rare_user = RareUsers.objects.get(pk=pk)
            serializer = BasicProfileSerializer(rare_user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def partial_update(self, request, pk=None):
        """Handle a partial update to a RareUser resource. Handles PATCH requests

        Currently this will only update the `active` property"""
        
        try:
            target_rare_user = RareUsers.objects.get(pk=pk)
        except RareUsers.DoesNotExist:
            return Response({'message': 'There is no user with the given Id'},
            status=status.HTTP_404_NOT_FOUND)

        if 'active' in request.data:
            #The client is trying to update the active property on the user
            #Only let them do it if they are an admin user
            if not request.auth.user.is_staff:
                return Response(
                    {'message': 'Only admin users can modify the active status of a user'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            target_rare_user.active = request.data["active"]
        
        try:
            target_rare_user.save()
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    """action to toggle between admin and author status depending on message from client"""
    @action(methods=['patch'], detail=True)
    def update_role(self, request, pk=None):
        try:
            rare_user = RareUsers.objects.get(pk=pk)
            user = rare_user.user
        except RareUsers.DoesNotExist:
            return Response({'message': 'user does not exit'}, status=status.HTTP_404_NOT_FOUND)
        if not request.auth.user.is_staff:
            return Response({'message':'only admins can change user roles'}, status=status.HTTP_403_FORBIDDEN)
        if request.data["is_staff"] == "false":
            user.is_staff = False
        else: 
            if request.data["is_staff"] == "true":
                user.is_staff = True
        try:
            user.save()
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_204_NO_CONTENT) 

class BasicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUsers
        fields = ('id', 'username', 'is_staff', 'active', 'email', 'created_on', 'profile_image_url', 'fullname' )
    



""" View module for handling requests about RareUsers"""

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rareapi.models import RareUsers


class RareUserView(ViewSet):
    """ Rare Users View Set """
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
            if not request.auth.is_staff:
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
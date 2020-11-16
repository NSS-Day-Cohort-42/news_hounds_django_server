from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import status
from django.core.exceptions import ValidationError

class ProfileViewSet(ViewSet):
    @action(methods=['patch'], detail=True)
    def update_role(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': 'user does not exit'}, status=status.HTTP_404_NOT_FOUND)
        if not request.auth.user.is_staff:
            return Response({'message':'only admins can change user roles'}, status=status.HTTP_403_FORBIDDEN)
        if user.is_staff:
            user.is_staff = False
        else:
            user.is_staff = True
        try:
            user.save()
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


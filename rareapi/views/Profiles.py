from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import status

class ProfileViewSet(ViewSet):
    @action(methods=['put'], detail=True)
    def update_role(self, request, pk=None):
        user = User.objects.get(pk=pk)
        if user.is_staff:
            user.is_staff = False
        else:
            user.is_staff = True
        user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
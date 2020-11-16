from django.http.response import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rareapi.models import RareUsers
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework import serializers

class ProfileViewSet(ViewSet):
    def list(self, request):
        users = RareUsers.objects.all()
        serializer = BasicProfileSerializer(users, many=True, context={'request':request})
        return Response(serializer.data)


    """PLEASE DISREGARD THE COMMENTED IT IS NOT UP TO STANDARDS"""
    # @action(methods=['patch'], detail=True)
    # def update_role(self, request, pk=None):
    #     try:
    #         user = User.objects.get(pk=pk)
    #     except User.DoesNotExist:
    #         return Response({'message': 'user does not exit'}, status=status.HTTP_404_NOT_FOUND)
    #     if not request.auth.user.is_staff:
    #         return Response({'message':'only admins can change user roles'}, status=status.HTTP_403_FORBIDDEN)
    #     if user.is_staff:
    #         user.is_staff = False
    #     else:
    #         user.is_staff = True
    #     try:
    #         user.save()
    #     except ValidationError as ex:
    #         return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

class BasicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUsers
        fields = ('id', 'username', 'is_staff', 'active')
    



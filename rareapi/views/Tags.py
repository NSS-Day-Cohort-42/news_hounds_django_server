from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareapi.models import Tags

class TagViewSet(ViewSet):
    def list(self, request):

        tags = Tags.objects.all()

        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        if not request.auth.user.is_staff:
            return Response(
                {'message': 'You must be an admin to create tags.'},
                status=status.HTTP_403_FORBIDDEN
            )

        tag = Tags()
        tag.label = request.data["label"]
        
        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            tag = Tags.objects.get(pk=pk)
        except Tags.DoesNotExist:
            return Response({'message':'tag not found'}, status=status.HTTP_404_NOT_FOUND)
        tag.label = request.data["label"]
        tag.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            tag = Tags.objects.get(pk=pk)
            tag.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Tags.DoesNotExist as ex:
            return Response({'message': ex.args[0]})
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""Basic Tag Serializer"""
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'label')
from rareapi.models import Reactions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers


class ReactionsViewSet(ViewSet):
    """Rare Reactions"""
    def list(self, request):
        reactions = Reactions.objects.all()
        serializer = ReactionSerializer(reactions, many=True, context={'request': request})
        try:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'message' : ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reactions
        fields = ('label', 'image_url', 'id')
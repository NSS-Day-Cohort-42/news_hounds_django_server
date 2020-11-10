
from rareapi.models.Comments import Comments
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comments

class CommentViewSet(ViewSet):



    def list(self, request):
        """Handle GET requests to comments resource
        Returns:
            Response -- JSON serialized list of comments
        """
        # SELECT * FROM levelupapi_game;
        comments = Comments.objects.all()

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    # def create(self, request):
    #     """Handle POST operations for commentss
    #     Returns:
    #         Response -- JSON serialized comments instance
    #     """
    #     rare_user = .objects.get(user=request.auth.user)

    #     comments = Comments()
    #     comments.post = request.data["post"]
    #     comments.author = request.data["author"]
    #     comments.content = request.data["content"]
    #     comments.subject = request.data["subject"]
    #     comments.created_on = request.data["created_on"]


    #     game = Game.objects.get(pk=request.data["gameId"])
    #     comments.game = game

    #     try:
    #         comments.save()
    #         serializer = commentsSerializer(comments, context={'request': request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except ValidationError as ex:
    #         return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comment creator"""

    class Meta:
        model = Comments
        fields = ('id','post','author', 'content', 'subject', 'created_on')




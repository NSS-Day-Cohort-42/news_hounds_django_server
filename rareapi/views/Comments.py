
from rareapi.models import Comments,Posts,RareUsers
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comments, Posts, RareUsers

class CommentViewSet(ViewSet):

    def create(self, request):
        """Handle POST operations for commentss
        Returns:
            Response -- JSON serialized comments instance
        """
        rare_user = RareUsers.objects.get(user=request.auth.user)
    
      

        comments = Comments()
        comments.post = request.data["post"]
        comments.author = request.data["author"]
        comments.content = request.data["content"]
        comments.subject = request.data["subject"]
        comments.created_on = request.data["created_on"]
        comments.rare_user = rare_user
        posts = Posts.objects.get(pk=request.data["post"])
        comments.post = posts

 

        try:
            comments.save()
            serializer = CommentSerializer(comments, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """Handle GET requests to comments resource
        Returns:
            Response -- JSON serialized list of comments
        """
        comments = Comments.objects.all()
        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     """Handle GET request for single Comment
    #     Returns:
    #         Response JSON serielized post instance
    #     """
    #     try:
    #         comments = Comments.objects.get(pk=pk)
    #         serializer = CommentSerializer(post, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comment creator"""

    class Meta:
        model = Comments
        fields = ('post','author', 'content', 'subject', 'created_on')





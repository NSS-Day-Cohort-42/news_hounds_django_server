
from rareapi.models import Comments,Posts,RareUsers
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comments, Posts, RareUsers
from django.utils import timezone
class CommentViewSet(ViewSet):

    def create(self, request):
        """Handle POST operations for commentss
        Returns:
            Response -- JSON serialized comments instance
        """
        rare_user = RareUsers.objects.get(user=request.auth.user)
    
        comments = Comments()
        comments.content = request.data["content"]
        comments.subject = request.data["subject"]
        comments.author = rare_user
        comments.created_on= timezone.now()
        posts = Posts.objects.get(pk=request.data["post_id"])
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
        post_id = request.query_params.get('post_id', None)
        if post_id is not None:
            comments = comments.filter(post_id = post_id)
        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

   

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comment creator"""

    class Meta:
        model = Comments
        fields = ( 'content', 'subject', 'created_on')

class RareUsersSerializer(serializers.ModelSerializer):
    """JSON serializer for rareUsers"""
    user = CommentSerializer(many=False)


    class Meta:
        model = RareUsers
        fields = ['user']

    class Meta:
        model = Posts
        fields = ['id']





""" View module for handling requests about posts"""
from django.http.response import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rareapi.models import Posts, RareUsers, Categories
from datetime import date
from django.core.exceptions import ValidationError

class PostViewSet(ViewSet):
    """Rare Posts"""
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized post instance
        """
        rare_user = RareUsers.objects.get(user=request.auth.user)
        post = Posts()
        post.user = rare_user

        #Try to assign the category to the post, but respond with an error if the category doesn't exist
        try: 
            category = Categories.objects.get(pk=request.data["category_id"])
            post.category = category
        except Categories.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
        post.title = request.data["title"]

        #Assign the publication date to be the current date
        post.publication_date = date.today()

        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        
        #Posts default to approved when created
        post.approved = True

        # Try to save the new post to the database, then
        # serialize the post instance as JSON, and send the
        # JSON as a response to the client request
        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """Handle GET requests to posts resource

        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Posts.objects.all()

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            posts = posts.filter(user_id=user_id)
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET request for single post
        Returns:
            Response JSON serielized post instance
        """
        try:
            post = Posts.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        try:
            post = Posts.objects.get(pk=pk)
            post.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Posts.DoesNotExist as ex:
            return Response({'message': ex.args[0]})
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostRareUserSerializer(serializers.ModelSerializer):
    """Serializer for RareUser Info in a post"""         
    class Meta:
        model = RareUsers
        fields = ('id', 'bio', 'fullname', 'username')

class PostSerializer(serializers.ModelSerializer):
    """Basic Serializer for single post"""
    user = PostRareUserSerializer(many=False)
    class Meta:
        model = Posts
        fields = ('id', 'title', 'publication_date', 'content', 'user', 'category', 'image_url', 'approved')
        depth = 1


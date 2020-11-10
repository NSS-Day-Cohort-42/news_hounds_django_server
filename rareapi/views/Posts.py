from django.http.response import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from rareapi.models import Posts, RareUsers

class PostViewSet(ViewSet):
    def list(self, request):

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
            

"""Serializer for RareUser Info in a post"""         
class PostRareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUsers
        fields = ('id', 'bio', 'fullname', 'username')

"""Basic Serializer for single post"""
class PostSerializer(serializers.ModelSerializer):
    user = PostRareUserSerializer(many=False)
    class Meta:
        model = Posts
        fields = ('id', 'title', 'publication_date', 'content', 'user', 'category')
        depth = 1


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

         
class PostRareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUsers
        fields = ('id', 'bio', 'fullname', 'username')

class PostSerializer(serializers.ModelSerializer):
    user = PostRareUserSerializer(many=False)
    class Meta:
        model = Posts
        fields = ('id', 'title', 'publication_date', 'content', 'user', 'category')
        depth = 1


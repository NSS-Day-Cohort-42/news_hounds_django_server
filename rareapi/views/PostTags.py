from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from rareapi.models import PostTags, Tags

class PostTagsViewSet(ViewSet):
    def list(self, request):

        posttags = PostTags.objects.all()

        post_id = self.request.query_params.get("postId", None)
        if post_id is not None:
            posttags = posttags.filter(post_id=post_id)
        
        serializer = PostTagsSerializer(posttags, many=True, context={'request', request})
        return Response(serializer.data)

class PostTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTags
        fields = ('id', 'tag')
        depth = 1

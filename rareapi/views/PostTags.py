from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareapi.models import PostTags, Tags, Posts

class PostTagsViewSet(ViewSet):
    def list(self, request):

        posttags = PostTags.objects.all()

        post_id = self.request.query_params.get("postId", None)
        if post_id is not None:
            posttags = posttags.filter(post_id=post_id)
        
        serializer = PostTagsSerializer(posttags, many=True, context={'request', request})
        return Response(serializer.data)

    def create(self, request):
        post_id = request.data["post_id"]
        post = Posts.objects.get(id=post_id)
        tag_id = request.data["tag_id"]
        tag = Tags.objects.get(id=tag_id)
        posttag = PostTags()
        posttag.post = post
        posttag.tag = tag
        try: 
            posttag.save()
            serializer = PostTagsSerializer(posttag, many=False, )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        

class PostTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTags
        fields = ('id', 'tag')
        depth = 1

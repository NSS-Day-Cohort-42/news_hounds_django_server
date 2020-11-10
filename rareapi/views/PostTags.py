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
        try:
            post = Posts.objects.get(id=post_id)
            tag_id = request.data["tag_id"]
            try: 
                tag = Tags.objects.get(id=tag_id)
                try:
                    posttag = PostTags.objects.get(post=post, tag=tag)
                    return Response({'message': 'PostTag already exists for these two items'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except PostTags.DoesNotExist:
                    posttag = PostTags()
                    posttag.post = post
                    posttag.tag = tag
                    try: 
                        posttag.save()
                        serializer = PostTagsSerializer(posttag, many=False, )
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    except ValidationError as ex:
                        return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
            except Tags.DoesNotExist:
                return Response({'message: invalid tag id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Posts.DoesNotExist:
            return Response({'message: invalid post id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def destroy(self, request, pk=None):
        try:
            posttag = PostTags.objects.get(pk=pk)
            posttag.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except PostTags.DoesNotExist as ex:
            return Response({'message': ex.args[0]})
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

class PostTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTags
        fields = ('id', 'tag', 'post')
        depth = 1

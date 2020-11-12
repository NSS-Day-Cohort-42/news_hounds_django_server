""" View module for handling requests about posts"""
from rareapi.models.PostTags import PostTags
from rareapi.models.Tags import Tags
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

        #extract tag ids from request and try to convert that collection to a queryset of actual tags
        tag_ids = request.data["tagIds"]

        try:
            tags = [Tags.objects.get(pk=tag_id) for tag_id in tag_ids]
        except Tags.DoesNotExist:
            return Response({'message': 'request contains a tagId for a non-existent tag'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # # Try to save the new post to the database, then
        # # serialize the post instance as JSON, and send the
        # # JSON as a response to the client request
        try:
            post.save()
        # # If anything went wrong, catch the exception and
        # # send a response with a 400 status code to tell the
        # # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        #for each tag
        for tag in tags:
            post_tag = PostTags(post=post, tag=tag)
            post_tag.save()

        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk=None):
        """ Handle an update request for a post

        'user', 'publication_date' and 'approved' attributes are not subject to change on update as currently configured 
        """

        ##Find the post being updated based on it's primary key  
        post = Posts.objects.get(pk=pk)

        #try to find the category that matches the one referenced in the request and save it as the post's 'category' value
        try: 
            category = Categories.objects.get(pk=request.data["category_id"])
            post.category = category
        except Categories.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        #save basic (non-associated) properties
        post.title = request.data["title"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]

        #extract tag ids from request and try to convert that collection to a queryset of actual tags
        request_tag_ids = request.data["tagIds"]
        try:
            request_tags = [ Tags.objects.get(pk=tag_id) for tag_id in request_tag_ids ]
        except Tags.DoesNotExist:
            return Response({'message': 'request contains a tagId for a non-existent tag'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        #save post object
        post.save()

        #look through all of the posttags in the DB, and assign those for which the post being updated is the 'post' attribute value to a new collection
        # (in other words, the current, pre-update collection of this post's associated 'posttags')
        current_posttags = PostTags.objects.filter(post=post)

        #create new queryset from the collection above that is ONLY those posttags for which the 'tag' attribute value doesn't match 
        #any of the tags specified in the request. Then delete them all. 
        current_posttags.exclude(tag__in=request_tags).delete()

        # for each tag in the set of 'tags' from the request, try to find an existing entry in the current_posttags that
        # matches that relationship; if one doesn't exist, create it
        for tag in request_tags:
            try:
                current_posttags.get(tag=tag)
            except PostTags.DoesNotExist:
                new_posttag = PostTags(post=post,tag=tag)
                new_posttag.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        

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
            

class PostRareUserSerializer(serializers.ModelSerializer):
    """Serializer for RareUser Info in a post"""         
    class Meta:
        model = RareUsers
        fields = ('id', 'bio', 'fullname', 'username')

class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'label')

class PostSerializer(serializers.ModelSerializer):
    """Basic Serializer for single post"""
    user = PostRareUserSerializer(many=False)
    tags = PostTagSerializer(many=True)
    class Meta:
        model = Posts
        fields = ('id', 'title', 'publication_date', 'content', 'user', 'category', 'image_url', 'approved', 'tags')
        depth = 1


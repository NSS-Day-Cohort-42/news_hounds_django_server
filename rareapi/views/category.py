"""Category ViewSet and Serializers"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.http.response import HttpResponseServerError
from rareapi.models import Categories

class CategoryViewSet(ViewSet):
    """Categories view set"""

    def create(self, request):
        """POST a new Categories object"""

        # VALIDATION:
        # Ensure that the user is an admin
        if not request.auth.user.is_staff:
            return Response(
                {'message': 'You must be an admin to create categories.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Ensure that client request included the required `label` key in POST body
        try:
            label = request.data['label']
        except KeyError:
            return Response(
                {'message': 'POST body must contain the `label` property.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure that client is not trying to save a category with a label that already exists
        try:
            # iexact - case-insensitive equality match
            Categories.objects.get(label__iexact=label)
            return Response(
                {'message': 'A category with that label already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # We were unable to find a category with that label, now let's save it
        except Categories.DoesNotExist:
            category = Categories(label=label)
            category.save()

            serialized_category = CategoriesSerializer(category)
            return Response(serialized_category.data, status=status.HTTP_201_CREATED)


    def list(self, request):
        """GET all categories"""
        categories = Categories.objects.all()

        serialized_categories = CategoriesSerializer(categories, many=True)
        return Response(serialized_categories.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """DELETE a category with the given pk"""

        try:
            category = Categories.objects.get(pk=pk)

        except Categories.DoesNotExist:
            return Response(
                {'message': 'There is no category with the specified ID.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if category.label == 'Uncategorized':
            return Response(
                {'message': 'Deleting the `Uncategorized` category is forbidden.'},
                status=status.HTTP_403_FORBIDDEN
            )

        category.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    
    def retrieve(self, request, pk=None):
        """Handle GET request for single post
        Returns:
            Response JSON serielized post instance
        """
        try:
            category = Categories.objects.get(pk=pk)
            serializer = CategoriesSerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Category, get the Category record
        # from the database whose primary key is `pk`
        category = Categories.objects.get(pk=pk)
        category.label = request.data["label"]
        

        category.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

class CategoriesSerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Categories
        fields = ('id', 'label')
        
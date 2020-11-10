"""Category ViewSet and Serializers"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from rareapi.models import Categories

class CategoryViewSet(ViewSet):
    """Categories view set"""

    def create(self, request):
        """POST a new Categories object"""

        # VALIDATION:
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

class CategoriesSerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Categories
        fields = ('id', 'label')
        
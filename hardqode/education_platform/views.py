
from .models import Product, Lesson, Group, Access
from .serializers import (
    ProductSerializer,
    LessonSerializer,
    GroupSerializer,
    ProductStatsSerializer
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing and editing Lesson instances.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @action(detail=True, methods=['get'])
    def by_product(self, request, pk=None):
        """
        Returns a list of Lessons for a specific Product.
        """
        user = request.user
        product_id = pk
        if Access.objects.filter(
                user=user,
                product_id=product_id
        ).exists():
            lessons = Lesson.objects.filter(product_id=product_id)
            serializer = self.get_serializer(
                lessons,
                many=True
            )
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Access to the requested product is denied."},
                status=403
            )


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProductStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing Product statistics.

    Provides statistics on the number of Lessons, Groups, and Access objects associated with each Product.

    ## Actions

    ### Retrieve

    Returns a list of Product statistics.

    ```
    GET /api/v1/products/stats/
    ```

    ### Example Response

    ```json
    [
        {
            "id": 1,
            "num_lessons": 3,
            "num_groups": 2,
            "num_access": 1
        },
        {
            "id": 2,
            "num_lessons": 5,
            "num_groups": 3,
            "num_access": 2
        }
    ]
    ```
    """
    queryset = Product.objects.all()
    serializer_class = ProductStatsSerializer

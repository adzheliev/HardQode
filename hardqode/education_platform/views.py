
from .models import Product, Lesson, Group, Access
from .serializers import ProductSerializer, LessonSerializer, GroupSerializer, ProductStatsSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @action(detail=True, methods=['get'])
    def by_product(self, request, pk=None):
        user = request.user
        product_id = pk
        if Access.objects.filter(user=user, product_id=product_id).exists():
            lessons = Lesson.objects.filter(product_id=product_id)
            serializer = self.get_serializer(lessons, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Access to the requested product is denied."}, status=403)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProductStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductStatsSerializer

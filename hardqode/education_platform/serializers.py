from rest_framework import serializers
from django.db.models import Count, Avg, F
from .models import Product, Group, Access, User, Lesson


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """

    # The number of lessons associated with a product
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'start_datetime',
            'cost',
            'creator',
            'lessons_count'
        ]

    def get_lessons_count(self, obj):
        """
        Returns the number of lessons associated with a product.
        """
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model.

    Attributes:
        id (int): The unique ID of the lesson.
        name (str): The name of the lesson.
        video_url (str): The URL of the video associated with the lesson.
        product (Product): The product that the lesson is associated with.
    """

    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'video_url',
            'product'
        ]


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the Group model.

    Attributes:
        id (int): The unique ID of the group.
        name (str): The name of the group.
        product (Product): The product that the group is associated with.
        users (list): A list of users that are part of the group.
    """

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'product',
            'users'
        ]


class ProductStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Attributes:
        id (int): The unique ID of the product.
        name (str): The name of the product.
        lessons_count (int): The number of lessons associated with the product.
        students_count (int): The number of students enrolled in the product.
        fill_percentage (float): The percentage of students enrolled in the product.
        purchase_percentage (float): The percentage of users who have purchased the product.
        min_users (int): The minimum number of users required to enroll in the product.
        max_users (int): The maximum number of users allowed to enroll in the product.

    Methods:
        get_lessons_count(self, obj): Returns the number of lessons associated with a product.
        get_students_count(self, obj): Returns the number of students enrolled in a product.
        get_fill_percentage(self, obj): Returns the percentage of students enrolled in a product.
        get_purchase_percentage(self, obj): Returns the percentage of users who have purchased a product.
    """

    def get_lessons_count(self, obj):
        """
        Returns the number of lessons associated with a product.

        Args:
            obj (Product): The product for which the number of lessons is to be returned.

        Returns:
            int: The number of lessons associated with the product.
        """
        return obj.lessons.count()

    def get_students_count(self, obj):
        """
        Returns the number of students enrolled in a product.

        Args:
            obj (Product): The product for which the number of students is to be returned.

        Returns:
            int: The number of students enrolled in the product.
        """
        return Access.objects.filter(product=obj).values('user').distinct().count()

    def get_fill_percentage(self, obj):
        """
        Returns the percentage of students enrolled in a product.

        Args:
            obj (Product): The product for which the percentage of students is to be returned.

        Returns:
            float: The percentage of students enrolled in the product.
        """
        groups = obj.groups.annotate(
            fill_level=Count('users') * 100.0 / F('max_users')
        )
        return groups.aggregate(Avg('fill_level'))['fill_level__avg'] or 0

    def get_purchase_percentage(self, obj):
        """
        Returns the percentage of users who have purchased a product.

        Args:
            obj (Product): The product for which the percentage of users is to be returned.

        Returns:
            float: The percentage of users who have purchased the product.
        """
        total_users = User.objects.count()
        users_with_access = (
            Access.objects.filter(product=obj).distinct().count()
        )
        return (users_with_access / total_users) * 100 if total_users else 0

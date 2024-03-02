from rest_framework import serializers
from django.db.models import Count, Avg, F
from .models import Product, Group, Access, User, Lesson


class ProductSerializer(serializers.ModelSerializer):
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
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'video_url',
            'product'
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'product',
            'users'
        ]


class ProductStatsSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'lessons_count',
            'students_count',
            'fill_percentage',
            'purchase_percentage',
            'min_users',
            'max_users'
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_students_count(self, obj):
        return Access.objects.filter(product=obj).values('user').distinct().count()

    def get_fill_percentage(self, obj):
        groups = obj.groups.annotate(
            fill_level=Count('users') * 100.0 / F('max_users')
        )
        return groups.aggregate(Avg('fill_level'))['fill_level__avg'] or 0

    def get_purchase_percentage(self, obj):
        total_users = User.objects.count()
        users_with_access = (
            Access.objects.filter(product=obj).distinct().count()
        )
        return (users_with_access / total_users) * 100 if total_users else 0

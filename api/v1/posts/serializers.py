from datetime import date

from rest_framework import serializers
from rest_framework.serializers import CurrentUserDefault, ModelSerializer

from category.models import get_permission_queryset
from posts.models import AcademicYear, Post


class PostSerializer(ModelSerializer):
    author = serializers.HiddenField(default=CurrentUserDefault())

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if not data["category"] in get_permission_queryset(
            self.context["request"].user
        ):
            raise serializers.ValidationError("В доступе отказано")
        return data

    def create(self, validated_data):
        post_category = validated_data.get("category")
        post_teacher = validated_data.get("teacher")
        data = validated_data.get("date")
        if not data:
            data = date.today()
        academic_year = AcademicYear.objects.filter(
            from_date__lte=data, to_date__gte=data
        ).last()
        count_post = Post.objects.filter(
            teacher=post_teacher, category=post_category, academic_years=academic_year
        ).count()
        if post_category.limit and count_post >= post_category.limit:
            raise serializers.ValidationError(
                f"У этого учителя {count_post} постов в этой категории."
            )
        return super(PostSerializer, self).create(validated_data)

    class Meta:
        model = Post
        fields = [
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "body_uz",
            "body_ru",
            "body_en",
            "category",
            "teacher",
            "author",
            "date",
            "indexing",
            "status",
        ]


class PostStatisticSerializer(ModelSerializer):
    author = serializers.HiddenField(default=CurrentUserDefault())
    category_name = serializers.CharField(source="category.name", read_only=True)
    year = serializers.SerializerMethodField(read_only=True)

    def get_year(self, obj):
        if 9 <= obj.date.month <= 12:
            return f"{obj.date.year}-{obj.date.year + 1}"
        return f"{obj.date.year - 1}-{obj.date.year}"

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if not data["category"] in get_permission_queryset(
            self.context["request"].user
        ):
            raise serializers.ValidationError("В доступе отказано")
        return data

    class Meta:
        model = Post
        fields = [
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "title",
            "category_name",
            "year",
            "body_uz",
            "body_ru",
            "body_en",
            "category",
            "teacher",
            "author",
            "date",
            "indexing",
            "status",
        ]

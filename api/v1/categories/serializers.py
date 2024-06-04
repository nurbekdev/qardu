from datetime import date

from django.contrib.auth.models import Group
from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers
from rest_framework.serializers import CurrentUserDefault

from category.models import Category


class CategorySerializer(TranslatableModelSerializer):
    author = serializers.HiddenField(default=CurrentUserDefault())
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = [
            "id",
            "author",
            "translations",
            "coefficient",
            "group",
            "limit",
        ]


class CategoryReportSerializer(TranslatableModelSerializer):
    point = serializers.FloatField(source="get_total_point")
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = ["id", "translations", "point"]


class GroupSerializer(serializers.ModelSerializer):
    point = serializers.SerializerMethodField()
    minus_point = serializers.SerializerMethodField()

    def get_academic_year(self):
        """Determines the current academic year based on the month and optional request parameter."""
        current_date = date.today()
        year = current_date.year + 1 if current_date.month > 8 else current_date.year

        request_year = self.context.get("request").GET.get("year")
        if request_year and request_year.isdigit():
            year = int(request_year)

        date_from = date(year=year - 1, month=9, day=1)
        date_to = date(year=year, month=8, day=31)
        return date_from, date_to

    def get_minus_point(self, obj):
        date_from, date_to = self.get_academic_year()

        total_point = sum(
            -category.get_total_points_date(date_from, date_to)
            for category in obj.category_set.filter(coefficient__lt=0)
        )
        return total_point

    def get_point(self, obj):
        date_from, date_to = self.get_academic_year()

        total_point = sum(
            category.get_total_points_date(date_from, date_to)
            for category in obj.category_set.filter(coefficient__gt=0)
        )
        return total_point

    class Meta:
        model = Group
        fields = ["id", "name", "point", "minus_point"]

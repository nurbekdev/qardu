from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from home.models import ControlLimit
from oauth.models import Teacher, TeacherLevel
from posts.models import Post


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "id",
            "first_name_uz",
            "first_name_ru",
            "first_name_en",
            "ext_date",
            "last_name_uz",
            "last_name_ru",
            "last_name_en",
            "father_name_uz",
            "father_name_ru",
            "father_name_en",
            "position_uz",
            "position_ru",
            "position_en",
            "image",
            "department",
            "level",
            "status",
            "uuid",
            "academic_title",
        ]

    def create(self, validated_data):
        teacher = super(TeacherSerializer, self).create(validated_data)
        if ControlLimit.objects.last():
            Post.objects.create(
                teacher=teacher,
                title_ru="Стартовый балл",
                body_ru="Стартовый балл",
                status=2,
                date=teacher.created,
                category=ControlLimit.objects.last().category,
                author=self.context["request"].user,
            )
        return teacher


class TeacherStatisticSerializer(ModelSerializer):
    total_point = SerializerMethodField(read_only=True)
    full_name = CharField(source="get_full_name", read_only=True)

    def get_total_point(self, obj):
        return obj.total_point

    class Meta:
        model = Teacher
        fields = [
            "id",
            "total_point",
            "position",
            "full_name",
            "first_name_uz",
            "first_name_ru",
            "first_name_en",
            "last_name_uz",
            "last_name_ru",
            "last_name_en",
            "father_name_uz",
            "father_name_ru",
            "father_name_en",
            "position_uz",
            "position_ru",
            "position_en",
            "image",
            "department",
            "level",
            "status",
            "uuid",
        ]

    def create(self, validated_data):
        teacher = super(TeacherStatisticSerializer, self).create(validated_data)
        if ControlLimit.objects.last():
            Post.objects.create(
                teacher=teacher,
                title_ru="Стартовый балл",
                body_ru="Стартовый балл",
                status=2,
                date=teacher.created,
                category=ControlLimit.objects.last().category,
                author=self.context["request"].user,
            )
        return teacher


class TeacherLevelSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=TeacherLevel)

    class Meta:
        model = TeacherLevel
        fields = ["id", "translations"]

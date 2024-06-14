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
            "firstname",
            "ext_date",
            "last_name",
            "father_name",
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
    fullname = CharField(source="get_full_name", read_only=True)

    def get_total_point(self, obj):
        return obj.total_point

    class Meta:
        model = Teacher
        fields = [
            "id",
            "total_point",
            "position",
            "fullname",
            "first_name",
            "last_name",
            "father_name",
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

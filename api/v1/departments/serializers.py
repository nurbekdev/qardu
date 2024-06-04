from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer

from home.models import Department


class DepartmentSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Department)

    class Meta:
        model = Department
        fields = ["id", "translations", "image"]

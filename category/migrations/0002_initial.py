# Generated by Django 3.2.14 on 2024-05-12 14:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("category", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="auth.group",
                verbose_name="Группа",
            ),
        ),
        migrations.AddField(
            model_name="academicpoints",
            name="academic_year",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="academic_points",
                to="posts.academicyear",
                verbose_name="Учебный год",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="statisticsscientifictranslation",
            unique_together={("language_code", "master")},
        ),
        migrations.AlterUniqueTogether(
            name="categorytypetranslation",
            unique_together={("language_code", "master")},
        ),
        migrations.AlterUniqueTogether(
            name="categorytranslation",
            unique_together={("language_code", "master")},
        ),
    ]

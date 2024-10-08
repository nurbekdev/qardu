# Generated by Django 3.2.14 on 2024-06-10 08:37

from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0005_auto_20240514_1650'),
        ('category', '0002_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academicyear',
            options={'ordering': ('-from_date',), 'verbose_name': "O'quv yili", 'verbose_name_plural': "O'quv yillari"},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Hujjat', 'verbose_name_plural': 'Hujjatlar'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-date',), 'verbose_name': 'Post', 'verbose_name_plural': 'Postlar'},
        ),
        migrations.AlterModelOptions(
            name='posttranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Post Translation'},
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='from_date',
            field=models.DateField(verbose_name='Boshlanish sanasi'),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='to_date',
            field=models.DateField(verbose_name='Tugash sanasi'),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='years',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Yil'),
        ),
        migrations.AlterField(
            model_name='document',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan'),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to=posts.models.upload_to_documents, verbose_name='Fayl'),
        ),
        migrations.AlterField(
            model_name='document',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='Post'),
        ),
        migrations.AlterField(
            model_name='document',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Yangilangan'),
        ),
        migrations.AlterField(
            model_name='post',
            name='academic_years',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.academicyear', verbose_name="O'quv yili"),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category', verbose_name='Kategoriya'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(verbose_name='Sana'),
        ),
        migrations.AlterField(
            model_name='post',
            name='indexing',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Indeksatsiya'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, "Ko'rib chiqilmoqda"), (2, 'Tasdiqlangan')], default=1, verbose_name='Holat'),
        ),
        migrations.AlterField(
            model_name='post',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oauth.teacher', verbose_name="O'qituvchi"),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Yangilangan'),
        ),
        migrations.AlterField(
            model_name='posttranslation',
            name='body',
            field=models.TextField(verbose_name='Matn'),
        ),
        migrations.AlterField(
            model_name='posttranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Sarlavha'),
        ),
    ]

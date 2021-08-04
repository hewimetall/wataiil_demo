# Generated by Django 3.2.5 on 2021-08-04 07:05

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_customimage_customrendition'),
        ('blog', '0013_auto_20210804_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostpage',
            name='header_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.customimage', verbose_name='Изображения в заголовке'),
        ),
        migrations.AlterField(
            model_name='blogpostpage',
            name='related_page',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='++', to='blog.blogpostpage', verbose_name='Предыдущая связанная новость'),
        ),
        migrations.AlterField(
            model_name='postpage',
            name='header_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.customimage', verbose_name='Изображения в заголовке'),
        ),
    ]
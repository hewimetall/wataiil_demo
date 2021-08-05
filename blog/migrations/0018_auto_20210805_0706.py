# Generated by Django 3.2.5 on 2021-08-05 07:06

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtailmarkdown.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_blogarticlepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticlepage',
            name='body',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(label='Загаловок')), ('paragraph', wagtail.core.blocks.RichTextBlock(label='Параграф')), ('markdown', wagtailmarkdown.blocks.MarkdownBlock(icon='code')), ('embed', wagtail.embeds.blocks.EmbedBlock(label='Внешний контент')), ('image', wagtail.images.blocks.ImageChooserBlock(label='Изображения')), ('quote', wagtail.core.blocks.BlockQuoteBlock(label='Цитата'))], blank=True, verbose_name='Контент на странице'),
        ),
        migrations.AlterField(
            model_name='blogpostpage',
            name='body',
            field=wagtail.core.fields.StreamField([('h2', wagtail.core.blocks.CharBlock(label='Загаловок')), ('paragraph', wagtail.core.blocks.RichTextBlock(label='Параграф')), ('markdown', wagtailmarkdown.blocks.MarkdownBlock(icon='code')), ('embed', wagtail.embeds.blocks.EmbedBlock(label='Внешний контент')), ('image', wagtail.images.blocks.ImageChooserBlock(label='Изображения')), ('quote', wagtail.core.blocks.BlockQuoteBlock(label='Цитата'))], blank=True, verbose_name='Контент на странице'),
        ),
    ]
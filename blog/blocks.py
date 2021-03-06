from wagtail.core.blocks import (
    BooleanBlock,
    CharBlock,
    ListBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    BlockQuoteBlock
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock
from wagtail.contrib.table_block.blocks import TableBlock

class ImageText(StructBlock):
    reverse = BooleanBlock(required=False)
    text = RichTextBlock()
    image = ImageChooserBlock()


class BodyBlock(StreamBlock):
    h1 = CharBlock()
    h2 = CharBlock()
    paragraph = RichTextBlock(label="Параграф")
    markdown = MarkdownBlock(icon="code")
    table = TableBlock()
    embed = EmbedBlock(label='Внешний контент')
    image_text = ImageText(label="Изображения")
    image_carousel = ListBlock(ImageChooserBlock(label="Изображения"), label="Карусель")
    thumbnail_gallery = ListBlock(ImageChooserBlock(label="Изображения"), label="Миниатюры")
    quote = BlockQuoteBlock(label='Цитата')

class OldBodyBlock(StreamBlock):
    h2 = CharBlock(label='Загаловок')
    paragraph = RichTextBlock(label="Параграф")
    markdown = MarkdownBlock(icon="code")
    embed = EmbedBlock(label='Внешний контент')
    image = ImageChooserBlock(label="Изображения")
    quote = BlockQuoteBlock(label='Цитата')
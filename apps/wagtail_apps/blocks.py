from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    ListBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """

    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a header size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """

    text = TextBlock()
    attribute_name = CharBlock(blank=True, required=False, label="e.g. Mary Berry")

    class Meta:
        icon = "openquote"
        template = "blocks/blockquote.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(icon="pilcrow", template="blocks/paragraph_block.html")
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
        template="blocks/embed_block.html",
    )


class BaseDailyPageStreamBlock(StreamBlock):
    source_code = RawHTMLBlock()
    big_title = CharBlock(max_length=512, help_text="大标题")
    content = RichTextBlock(help_text="内容")
    ico_image = ImageChooserBlock(help_text="头像")
    author_name = CharBlock(max_length=255, help_text="作者")
    author_intro = CharBlock(max_length=255, help_text="作者介绍")


class BasePageStreamBlock(StreamBlock):
    source_code = RawHTMLBlock()
    big_title = CharBlock(max_length=512, help_text="大标题")
    content = ListBlock(
        RichTextBlock(help_text="内容"), help_text="这里可以填入多个内容，也可以只填写一个"
    )

    author_info = StructBlock(
        [
            ("ico_image", ImageChooserBlock(help_text="头像")),
            ("author_name", CharBlock(max_length=255, help_text="作者")),
            ("author_intro", CharBlock(max_length=255, help_text="作者介绍")),
        ],
        null=True,
        blank=True,
        max_num=1,
        help_text="作者信息",
    )

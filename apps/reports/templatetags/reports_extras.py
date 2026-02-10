import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def markdown_content(value):
    """Convert markdown to HTML"""
    if not value:
        return ""
    return mark_safe(
        markdown.markdown(
            value,
            extensions=["markdown.extensions.fenced_code", "markdown.extensions.tables"],
            output_format="html5",
        )
    )

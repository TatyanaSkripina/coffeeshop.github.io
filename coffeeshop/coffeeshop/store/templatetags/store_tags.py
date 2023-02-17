from django import template
from store.models import Category

register = template.Library()

@register.simple_tag()
def get_categories():
    # categories = Category.objects.all()
    # for category in categories:
    #     print(category.products.all())
    return Category.objects.all()
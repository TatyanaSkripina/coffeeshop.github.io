from django.contrib import admin
from .models import Category, Product, Size


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    prepopulated_fields = {'slug': ('title',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'price', 'size']
    prepopulated_fields = {'slug': ('title',)}

# class SizeAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Size)





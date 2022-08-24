from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, Image, Star, StarForProduct, Reviews, \
    Room, Message


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('user',)


class ToyImage(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.link.url} width="100" height="110"')

    get_image.short_description = 'Изображение'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'get_image', 'quantity', 'is_active']
    list_display_links = ['name']
    search_fields = ['name', 'category__name']
    list_editable = ('is_active',)
    inlines = [ToyImage, ReviewInline]
    save_on_top = True
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    get_image.short_description = 'Постер'


class ImageAdmin(admin.ModelAdmin):
    list_display = ['link', 'product', 'get_image']
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.link.url} width="50" height="60"')


class StarAdmin(admin.ModelAdmin):
    list_display = ['star']


class StarForProductAdmin(admin.ModelAdmin):
    list_display = ['star', 'product']


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'created', 'product']
    search_fields = ['user', 'created', 'description']


class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'admin', 'user']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'date']
    search_fields = ['user']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Star, StarAdmin)
admin.site.register(StarForProduct, StarForProductAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)

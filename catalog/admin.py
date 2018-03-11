from django.contrib import admin
from .models import (Category, Tag, Catalog, Offer, OfferItem, MediaResource)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'description', 'active',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'active',)


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'start_date', 'end_date', 'provider',
                    'active')


@admin.register(OfferItem)
class OfferItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'offer',)


@admin.register(MediaResource)
class MediaResourceAdmin(admin.ModelAdmin):
    list_display = ('label', 'offer',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'catalog', 'active',)

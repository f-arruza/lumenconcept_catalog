from rest_framework import serializers

from .models import (Category, Tag, Item)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class ItemDetailsSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Item
        fields = (
            'id',
            'code',
            'name',
            'description',
            'image',
            'score',
            'price',
            'provider_id',
            'category',
            'tags',
        )

    @classmethod
    def get_category(self, obj):
        try:
            return obj.category.name
        except:
            return None


class CategoryDetailsSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            'id',
            'code',
            'name',
            'description',
            'type',
        )

    @classmethod
    def get_type(self, obj):
        try:
            return obj.get_type_display()
        except:
            return None

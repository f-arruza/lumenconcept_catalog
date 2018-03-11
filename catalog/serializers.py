import requests, decimal

from rest_framework import serializers

from django.conf import settings
from django.db import DatabaseError, transaction

from .models import (Category, Tag, Catalog, Offer, OfferItem, MediaResource)
from .utils import send_message_rabbit, send_message_sqs


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = '__all__'


class OfferItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferItem
        fields = '__all__'


class OfferItemDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferItem
        fields = (
            'id',
            'item',
            'count',
        )


class MediaResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaResource
        fields = '__all__'


class MediaResourceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaResource
        fields = (
            'id',
            'label',
            'path',
        )

class OfferItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferItem
        fields = (
            'item',
            'count',
        )

class OfferCreateSerializer(serializers.ModelSerializer):
    items = OfferItemCreateSerializer(many=True)
    resources = MediaResourceDetailSerializer(many=True)

    data = {}

    class Meta:
        model = Offer
        fields = (
            'title',
            'description',
            'catalog',
            'price',
            'reference_price',
            'stock',
            'threshold',
            'tags',
            'items',
            'resources',
        )

    def validate_items(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("You must register at least one item.")

        for i in value:
            code = i.get('item')
            url = settings.URL_PRODUCT_MICROSERVICE + 'products/code/' + code
            response = requests.get(url)
            if response.status_code == 404:
                raise serializers.ValidationError("Item " + code + " not found.")

            self.data[code] = response.json()
        return value

    def create(self, validated_data):
        try:
            # Atomic Transaction
            with transaction.atomic():
                offer = Offer(title=validated_data.get('title'),
                              description=validated_data.get('description'),
                              catalog=validated_data.get('catalog'),
                              price=validated_data.get('price'),
                              reference_price=validated_data.get('reference_price'),
                              stock=validated_data.get('stock'),
                              threshold=validated_data.get('threshold'))
                offer.save()

                # Añadir Tags
                tags = validated_data.get('tags')
                for t in tags:
                    offer.tags.add(t)

                # Añadir OfferItems
                oitems = validated_data.get('items')
                for i in oitems:
                    oitem = OfferItem(item=i.get('item'), offer=offer)
                    if i.get('count') is not None:
                        oitem.count = i.get('count')
                    oitem.save()

                # Añadir MediaResources
                resources = validated_data.get('resources')
                for r in resources:
                    resource = MediaResource(label=r.get('label'), offer=offer,
                                             path=r.get('path'))
                    resource.save()

                # Consultar información del proveedor
                provider_code = offer.catalog.provider
                provider_name = ''
                provider_location = ''
                provider_score = ''

                url = settings.URL_PROVIDER_MICROSERVICE + 'providers/code/' + provider_code

                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    provider_name = data['name']
                    provider_location = data['city'] + ", " + data['country']
                    provider_score = data['score']

                registry_detail = {
                    "type": "CATALOG_SEARCH",
                    "catalog_name": offer.catalog.name,
                    "catalog_description": offer.catalog.description,
                    "catalog_category": offer.catalog.category.name,
                    "provider_code": provider_code, # b72587f2-26d0-4a38-a91b-0dfa50bf7afa
                    "provider_name": provider_name,
                    "provider_location": provider_location,
                    "provider_score": provider_score,
                    "offer_code": str(offer.code),
                    "offer_title": offer.title,
                    "offer_description": offer.description,
                    "offer_price": str(offer.price),
                    "offer_reference_price": str(offer.reference_price),
                    "offer_discount": str(offer.discount.quantize(decimal.Decimal(10) ** -2)),
                    "offer_stock": offer.stock,
                    "offer_threshold": offer.threshold,
                    "offer_tags": [],
                    "offer_items": []
                }
                # Añadir Tags
                for tag in offer.tags.all():
                    registry_detail['offer_tags'].append(tag.name)

                # Añadir OfferItems
                for i in offer.items.all():
                    data = self.data[i.item]
                    item_detail = {
                        "product_code": data['code'],
                        "product_reference": data['reference'],
                        "product_name": data['name'],
                        "product_description": data['description'],
                        "product_category": data['category'],
                        "product_score": data['score']
                    }
                    registry_detail['offer_items'].append(item_detail)

                # Publicar en SQS (catalog_append)
                send_message_sqs('catalog_append', str(registry_detail))
                return offer
        except DatabaseError:
            raise serializers.ValidationError("Error when trying to register the offer.")


class OfferDetailSerializer(serializers.ModelSerializer):
    id_catalog = serializers.SerializerMethodField()
    catalog = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    items = OfferItemDetailSerializer(many=True)
    resources = MediaResourceDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = (
            'id',
            'code',
            'title',
            'description',
            'id_catalog',
            'catalog',
            'price',
            'reference_price',
            'discount',
            'stock',
            'threshold',
            'tags',
            'items',
            'resources',
        )

    @classmethod
    def get_id_catalog(self, obj):
        try:
            return obj.catalog.id
        except:
            return None

    @classmethod
    def get_catalog(self, obj):
        try:
            return obj.catalog.name
        except:
            return None

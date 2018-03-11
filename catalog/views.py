from catalog import urls

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import response, schemas
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes

from .utils import send_message_sqs
from .models import (Category, Tag, Catalog, Offer, OfferItem, MediaResource)
from .serializers import (CategorySerializer, TagSerializer, CatalogSerializer,
                          OfferSerializer, OfferItemSerializer,
                          MediaResourceSerializer, OfferDetailSerializer,
                          OfferCreateSerializer)


@api_view()
@permission_classes((AllowAny, ))
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='LumenConcept Catalog API Docs',
                                        patterns=urls.api_url_patterns,
                                        url='/api/v1/')
    return response.Response(generator.get_schema())


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(active=True)

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name', 'description',
    )


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.filter(active=True)

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
    )


class CatalogViewSet(viewsets.ModelViewSet):
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.filter(active=True)

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name', 'description',
    )


class OfferItemViewSet(viewsets.ModelViewSet):
    serializer_class = OfferItemSerializer
    queryset = OfferItem.objects.all()


class MediaResourceViewSet(viewsets.ModelViewSet):
    serializer_class = MediaResourceSerializer
    queryset = MediaResource.objects.all()


class OfferViewSet(viewsets.ModelViewSet):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'title', 'description', 'tags',
    )

    def list(self, request):
        queryset = Offer.objects.filter(active=True)

        serializer = OfferSerializer(self.queryset, many=True)
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        else:
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Offer.objects.all()
        offer = get_object_or_404(queryset, pk=pk)
        offer.active = False
        offer.save()

        registry_detail = {
            "offer_code": str(offer.code)
        }
        print(registry_detail)
        # Publicar en SQS (catalog_append)
        send_message_sqs('catalog_remove', str(registry_detail))

        serializer = OfferSerializer(offer)
        return Response(serializer.data)

    def create(self, request):
        serializer = OfferCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        obj = serializer.save()
        serializer = OfferDetailSerializer(obj)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Offer.objects.all()
        offer = get_object_or_404(queryset, pk=pk)
        serializer = OfferDetailSerializer(offer)
        return Response(serializer.data)

    def retrieve_code(self, request, code):
        queryset = Offer.objects.filter(code=code, active=True)
        offer = get_object_or_404(queryset)
        serializer = OfferDetailSerializer(offer)
        return Response(serializer.data)

from catalog import urls

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import response, schemas
from rest_framework.permissions import AllowAny
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes

from .models import (Category, Tag, Item)
from .serializers import ItemSerializer, CategorySerializer, TagSerializer


@api_view()
@permission_classes((AllowAny, ))
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='LumenConcept API Docs',
                                        patterns=urls.api_url_patterns,
                                        url='/api/v1/')
    return response.Response(generator.get_schema())


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name', 'description', 'category',
    )


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name', 'description',
    )


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
    )

from catalog import urls

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import response, schemas
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes

from .models import (Category, Tag, Item)
from .serializers import (ItemSerializer, CategorySerializer, TagSerializer,
                          ItemDetailsSerializer, CategoryDetailsSerializer)


@api_view()
@permission_classes((AllowAny, ))
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='LumenConcept Catalog API Docs',
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

    def list(self, request):
        queryset = Item.objects.filter(active=True)

        serializer = ItemDetailsSerializer(self.queryset, many=True)
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        else:
            return Response(serializer.data)

    def retrive_list(self, request):
        param = request.data
        try:
            items = param['items']
            queryset = Item.objects.filter(pk__in=items)

            serializer = ItemDetailsSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            response = { 'error' : 'Solicitud incorrecta.' }
            return JsonResponse(response, safe=False)

    def retrieve(self, request, pk=None):
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ItemDetailsSerializer(item)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name', 'description',
    )

    def list(self, request):
        queryset = Category.objects.filter(active=True)

        serializer = CategoryDetailsSerializer(self.queryset, many=True)
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        else:
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        categ = get_object_or_404(queryset, pk=pk)
        serializer = CategoryDetailsSerializer(categ)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name',
    )

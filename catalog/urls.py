from django.conf.urls import url, include

from .views import (schema_view, ItemViewSet, CategoryViewSet, TagViewSet)

api_url_patterns = [
    url(r'^items/$', ItemViewSet.as_view({
                                           'get': 'list',
                                           'post': 'create',
                                          }), name='items-list'),
    url(r'^items/(?P<pk>[0-9]+)$', ItemViewSet.as_view({
                                                   'get': 'retrieve',
                                                   'put': 'update',
                                                   'patch': 'partial_update',
                                                   'delete': 'destroy'
                                                  }), name='items'),
    url(r'^categories/$', CategoryViewSet.as_view({
                                                   'get': 'list',
                                                   'post': 'create',
                                                  }), name='category-list'),
    url(r'^categories/(?P<pk>[0-9]+)$', CategoryViewSet.as_view({
                                                   'get': 'retrieve',
                                                   'put': 'update',
                                                   'patch': 'partial_update',
                                                   'delete': 'destroy'
                                                  }), name='category'),
    url(r'^tags/$', TagViewSet.as_view({
                                           'get': 'list',
                                           'post': 'create',
                                          }), name='tag-list'),
    url(r'^tags/(?P<pk>[0-9]+)$', TagViewSet.as_view({
                                                   'get': 'retrieve',
                                                   'put': 'update',
                                                   'patch': 'partial_update',
                                                   'delete': 'destroy'
                                                  }), name='tag'),
]


urlpatterns = [
    url(r'^api/v1/', include(api_url_patterns)),
    url(r'^', schema_view),
]

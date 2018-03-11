from django.conf.urls import url, include

from .views import (schema_view, CatalogViewSet, CategoryViewSet, TagViewSet,
                    OfferItemViewSet, MediaResourceViewSet, OfferViewSet)

api_url_patterns = [
    url(r'^catalogs/$', CatalogViewSet.as_view({
                                               'get': 'list',
                                               'post': 'create',
                                               }), name='catalogs-list'),
    url(r'^catalogs/(?P<pk>[0-9]+)$', CatalogViewSet.as_view({
                                                   'get': 'retrieve',
                                                   'put': 'update',
                                                   'patch': 'partial_update',
                                                   'delete': 'destroy'
                                                  }), name='catalogs'),
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
    url(r'^mediaresources/$', MediaResourceViewSet.as_view({
                                                           'get': 'list',
                                                           'post': 'create',
                                                           }), name='media-list'),
    url(r'^mediaresources/(?P<pk>[0-9]+)$', MediaResourceViewSet.as_view({
                                                                         'get': 'retrieve',
                                                                         'put': 'update',
                                                                         'patch': 'partial_update',
                                                                         'delete': 'destroy'
                                                                         }), name='media'),
    url(r'^offeritems/$', OfferItemViewSet.as_view({
                                                   'get': 'list',
                                                   'post': 'create',
                                                   }), name='offeritem-list'),
    url(r'^offeritems/(?P<pk>[0-9]+)$', OfferItemViewSet.as_view({
                                                                 'get': 'retrieve',
                                                                 'put': 'update',
                                                                 'patch': 'partial_update',
                                                                 'delete': 'destroy'
                                                                 }), name='offeritem'),
    url(r'^offers/$', OfferViewSet.as_view({
                                           'get': 'list',
                                           'post': 'create',
                                           }), name='offer-list'),
    url(r'^offers/code/(?P<code>[\w-]+)$', OfferViewSet.as_view({
                                                         'get': 'retrieve_code'
                                                         }), name='offer-retrieve'),
    url(r'^offers/(?P<pk>[0-9]+)$', OfferViewSet.as_view({
                                                         'get': 'retrieve',
                                                         'put': 'update',
                                                         'patch': 'partial_update',
                                                         'delete': 'destroy'
                                                         }), name='offer'),
]


urlpatterns = [
    url(r'^api/v1/', include(api_url_patterns)),
    url(r'^', schema_view),
]

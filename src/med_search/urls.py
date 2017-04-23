from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

import citations.api
import search.api

router = routers.SimpleRouter()
search_router = routers.DefaultRouter()


router.register(
    'citations', citations.api.CitationViewSet, 'citations'
)
search_router.register(
    'citations', citations.api.CitationIndexViewSet, 'citations'
)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls, namespace="api")),
    url(r'^search/$', search.api.SearchView.as_view(), name="search"),
    url(r'^search/', include(search_router.urls, namespace="search")),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^rosetta/', include('rosetta.urls')),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

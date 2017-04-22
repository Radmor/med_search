from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

import citations.api

router = routers.SimpleRouter()
search_router = routers.SimpleRouter()

router.register(
    'citations', citations.api.CitationViewSet, 'citations'
)
search_router.register(
    'citations', citations.api.CitationIndexViewSet, 'citations'
)
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'api/', include(router.urls)),
    url(r'search/', include(search_router.urls)),
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

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.http import HttpResponse

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blota.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url(r'^', include('question.urls')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


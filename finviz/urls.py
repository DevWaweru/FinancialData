from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.home, name='home'),
    url(r'^country/(?P<country>\w+)/$', views.country, name='country'),
    url(r'^company/(?P<company>\w+)/$', views.single_company, name='company'),
    url(r'^sector/(?P<sector>\w+)/$', views.sector, name='sector')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
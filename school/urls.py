from django.conf.urls import url
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^panthers', views.panthers, name="panthers"),
    url(r'^lions', views.lions, name="lions"),
    url(r'^tigers', views.tigers, name="tigers"),
    url(r'^jaguars', views.jaguars, name="jaguars"),
    url(r'^overview', views.overview, name="overview"),
    url(r'^core', admin.site.urls),
    url(r'^(?P<event_id>\d+)', views.event_details, name="event_details"),
    url(r'^get', views.main, name="main"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
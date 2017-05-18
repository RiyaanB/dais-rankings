"""DaisHouseEventInterface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponse

#import password_requred
#from decorator_include import decorator_include

def redirect(request):
    return HttpResponse("<meta http-equiv=\"refresh\" content=\"0; url=/home\" />")

urlpatterns = [
    #url(r'^core/main', decorator_include(password_required, "school.urls")),
    url(r'^core/', admin.site.urls),
    url(r'^$', redirect, name="redirect"),
    url(r'^home/$', include('school.urls')),
    url(r'^houses/', include('school.urls')),
    url(r'^school/events/', include('school.urls'))
]

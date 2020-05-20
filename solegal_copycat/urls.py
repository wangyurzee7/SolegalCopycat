"""solegal_copycat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
admin.autodiscover()
from django.conf.urls import url

from . import view

from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', view.index),
	# url(r'index/', view.index),
	url(r'search/authoritative/$',view.search_authoritative),
    url(r'search/common/$',view.search_common),
    url(r'detail/authoritative/', view.detail_authoritative),
    url(r'detail/common/', view.detail_common),
]

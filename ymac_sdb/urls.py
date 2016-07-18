"""ymac_sdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib.gis import admin
from ymac_db import views

urlpatterns = [
    url(r'^home/', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^services/$', views.services, name='services'),
    url(r'^software/$', views.software, name='software'),
    url(r'^workbenches/$', views.workbenches, name='workbenches'),
    url(r'^workbenches/data_download/$', views.data_download, name='datadownload'),
    url(r'^workbenches/region_distance/$', views.RegionDistanceView.as_view()),
    url(r'^spatial_request/$', views.SpatialRequestView.as_view()),
    url(r'^sites/', views.get_site),
    url(r'^heritage_surveys/', views.SurveyView.as_view()),
    url(r'^heritagesurvey-autocomplete/$', views.HeritageSurveyAutocomplete.as_view(),
        name='heritagesurvey-autocomplete'),
    url(r'^surveytrip-autocomplete/$', views.HeritageSurveyTripAutocomplete.as_view(),
        name='surveytrip-autocomplete'),
    url(r'^', admin.site.urls),
]

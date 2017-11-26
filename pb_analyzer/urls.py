from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^summoners/([0-9,]+)/$', views.analyze, name='analyze')
]

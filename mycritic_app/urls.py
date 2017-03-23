from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search/', views.result, name='result'),
    url(r'^$', views.search, name='search'),
]

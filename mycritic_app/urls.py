from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search/', views.result, name='result'),
    url(r'^$', views.search, name='search'),
    # Registration URLs
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register/complete/$', views.registration_complete, name='registration_complete'),
]

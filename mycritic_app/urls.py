from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    url(r'^result/', views.result, name='result'),
    url(r'^search/$', views.search, name='search'),
    # Registration URLs
    url(r'^register/$', views.register, name='register'),
    url(r'^register/complete/$', views.registration_complete, name='registration_complete'),
    # Auth-related URLs:
    url(r'^login/$', views.login, name='login'),
    url(r'^$', views.logged_in, name='home'),
    url(r'^login_error/$', views.login_error, name='login_error'),
    url(r'^logout/$', views.logout, name='logout'),
]

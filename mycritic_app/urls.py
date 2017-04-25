from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    url(r'^search/', views.result, name='result'),
    url(r'^$', views.search, name='search'),
    # Registration URLs
    url(r'^register/$', views.register, name='register'),
    url(r'^register/complete/$', views.registration_complete, name='registration_complete'),
    # Auth-related URLs:
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^loggedin/$', views.logged_in, name='loggedin'),
]

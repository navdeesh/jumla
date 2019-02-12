from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('logout', views.logout, name='logout'),
]
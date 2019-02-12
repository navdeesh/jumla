from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('logout', views.logout, name='logout'),
    path('get_content', views.get_content, name='get_content'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('my_subscriptions', views.my_subscriptions, name='my_subscriptions'),
]
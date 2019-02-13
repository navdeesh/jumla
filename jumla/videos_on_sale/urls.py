from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('do_logout', views.do_logout, name='do_logout'),
    path('show_content/<str:video_or_videopack>/<int:content_id>', views.show_content, name='show_content'),
    path('view_content/<str:video_or_videopack>/<int:content_id>/<str:duration>', views.view_content, name='view_content'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('logout', views.logout, name='logout'),
    path('get_content', views.get_content, name='get_content'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('my_subscriptions', views.my_subscriptions, name='my_subscriptions'),
    path('my_subscriptions_page', views.my_subscriptions_page, name='my_subscriptions_page'),    
    path('get_add_ons/<int:id>/<str:duration>', views.get_add_ons, name='get_add_ons'),
    path('subscribe_to_add_on/<int:id>/<str:duration>/<int:amount>', views.subscribe_to_add_on, name='subscribe_to_add_on'),
]
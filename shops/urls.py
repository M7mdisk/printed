from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name ='main'),
    path('order/<str:pk>/',views.create_order, name = 'order'),
    path('register/',views.register, name='register'),
    path('register/owner/',views.registerOwner, name='register_owner'),
    path('login/',auth_views.LoginView.as_view(template_name='shops/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='shops/logout.html'), name='logout'),
    path('dash/',views.OrdersList.as_view(), name='dash'),
    path('dash/<str:pk>/',views.OrdersList.as_view(), name='dash_shop'),
    path('orders/',views.my_orders, name='orders'),
    path('about/',views.about, name='about'),
    path('newshop/',views.create_shop, name='newshop'),

]

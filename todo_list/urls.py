from django.urls import path
from . import views
from .views import ContactView

urlpatterns = [
    path('', views.home, name='home'),
    path('stockmarket/', views.stockmarket, name='stockmarket'),
    path('marketnews/', views.marketnews, name='marketnews'),
    path('cryptocurrency/', views.cryptocurrency, name='cryptocurrency'),
    path('mailinbox/', views.mailinbox, name='mailinbox'),
    path('authlogin/', views.authlogin, name='authlogin'),
    path('authregister/', views.authregister, name='authregister'),
    path('logout/', views.logout, name='logout'),
    path('contact', ContactView.as_view(), name='contact')
]

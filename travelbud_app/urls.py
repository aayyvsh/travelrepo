from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('trips', views.trips),
    path('login', views.login), 
    path('trips/add', views.addtrip),
    path('logout', views.logout),
    path('createtrip', views.createtrip),
    path('jointrip/<tripID>', views.jointrip),
    path('location/<tripID>', views.location)
]
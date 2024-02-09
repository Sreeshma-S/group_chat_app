from django.urls import path

from . import views

urlpatterns = [
    path('', views.chatrooms, name='chatrooms'),
    path('<slug:slug>/', views.chatroom, name='chatroom'),
]
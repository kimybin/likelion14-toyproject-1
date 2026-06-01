from django.urls import path
from . import views

urlpatterns = [
    path('', views.relay, name='relay'),
    path('invite/', views.invite, name='invite'),
    path('certification/<int:slot_id>/', views.certification, name='certification'),
]
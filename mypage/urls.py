from django.urls import path
from . import views

urlpatterns = [
    path('', views.mypage, name='mypage'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('delete/', views.delete_account, name='delete_account'),
]
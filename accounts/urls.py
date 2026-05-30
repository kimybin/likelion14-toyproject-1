from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_home_view, name='login_home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('goal/', views.goal_view, name='goal'),
    path('goal/custom/', views.goal_custom_view, name='goal_custom'),
    path('team/name/', views.team_name_view, name='team_name'),
    path('team/join/', views.team_join_view, name='team_join'),

]
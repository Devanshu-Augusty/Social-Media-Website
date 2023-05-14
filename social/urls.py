from django.urls import path
from social import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('settings/', views.settings, name = 'settings'),
    path('upload/', views.upload, name = 'upload'),
    path('profile/<str:pk>/', views.profile, name = 'profile'),
    path('follow', views.follow, name = 'follow'),
    path('likes/', views.likes, name = 'likes'),
    path('search', views.search, name = 'search'),
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
]
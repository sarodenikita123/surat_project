from django.urls import path
from .views import *

urlpatterns = [
    path( 'user/', UserAPI.as_view()),
    path( 'user/<pk>/', UserAPI.as_view()),
    path( 'login/' , LoginView.as_view() ),
	path( 'logout/' , LogoutView.as_view()),
    path( 'change/<pk>/' , ChangeUserRoleView.as_view()),
    path( 'role/' , UserRoleView.as_view()),
	path( 'role/<pk>/' , UserRoleView.as_view()),

]

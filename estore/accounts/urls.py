from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('', views.Dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('my_orders/', views.my_orders, name="my_orders"),
    path('edit_profile/', views.EditProfile, name="edit_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('order_details/<int:order_id>/', views.order_details, name="order_details"),


]

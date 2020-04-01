from django.urls import path
from . import views

urlpatterns = [
    path('register.html', views.register, name='register'),
    path('login.html', views.login_view, name='login'),
    path('accounts/login/',views.login_view, name='login2'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('myStocks.html', views.myStocks, name='myStocks'),
    path('delete/<stock_id>', views.deleteStock, name="deleteStock")
]

# Include will allow us to incude
# other files in this project for paths
from django.urls import path
from . import views
from register import views as view

urlpatterns = [
    # Homepage Path
    path('',views.home, name='home'),
    # About me page path
    path('about.html',views.about,name='about'),
    # My Portfolio page
    path('myStocks.html',views.myStocks, name='myStocks'),
    path('register',view.register, name='register'),

]

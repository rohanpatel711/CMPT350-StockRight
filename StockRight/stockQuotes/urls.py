# Include will allow us to incude
# other files in this project for paths
from django.urls import path
from . import views

urlpatterns = [
    # Homepage Path
    path('',views.home, name='home'),
    # About me page path
    path('about.html',views.about,name='about'),
]

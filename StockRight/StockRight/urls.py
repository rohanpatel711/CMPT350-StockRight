from django.contrib import admin
# Include will allow us to incude
# other files in this project for paths
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Homepage Path
    path('',include('stockQuotes.urls')),
    path('',include('StockNews.urls')),
]

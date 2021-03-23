from django.urls import path, include  
from django.contrib import admin  
  
  
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('', include('blogapp.urls', namespace='blogapp')),  
]
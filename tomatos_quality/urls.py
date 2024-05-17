



from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('tomatos_a.urls')),
    path('admin/', admin.site.urls),
]

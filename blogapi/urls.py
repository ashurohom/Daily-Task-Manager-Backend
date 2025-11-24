from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.core.management import call_command

def home(request):
    return JsonResponse({"message": "Backend Running Successfully!"})

def run_migrations(request):
    call_command("migrate")
    return JsonResponse({"message": "Migrations completed!"})

urlpatterns = [
    path('', home),                          # Homepage JSON message
    path('admin/', admin.site.urls),         # Admin panel
    path('api/posts/', include('posts.urls')),  # Posts API
    path('run-migrations/', run_migrations), # Manual migrations URL
]

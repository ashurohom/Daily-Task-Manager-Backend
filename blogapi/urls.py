from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.core.management import call_command
from posts import views

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
    path('run-migrations/', views.run_migrations),  # Use this instead
]


# Base URL : https://daily-task-manager-backend-production.up.railway.app/
# Admin Panel : https://daily-task-manager-backend-production.up.railway.app/admin/
# Create Post : https://daily-task-manager-backend-production.up.railway.app/api/posts/create/
# List Posts : https://daily-task-manager-backend-production.up.railway.app/api/posts/list/
# Update Post : https://daily-task-manager-backend-production.up.railway.app/api/posts/update/1/
# Delete Post : https://daily-task-manager-backend-production.up.railway.app/api/posts/delete/1/
# Run Migrations : https://daily-task-manager-backend-production.up.railway.app/run-migrations/